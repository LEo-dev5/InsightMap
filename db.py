import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def save_snapshot(date, nodes, edges):
    with engine.connect() as conn:
        # 1. 스냅샷 저장
        result = conn.execute(
            text("INSERT INTO snapshots (date) VALUES (:date) ON CONFLICT (date) DO UPDATE SET date=:date RETURNING id"),
            {"date": date}
        )
        snapshot_id = result.fetchone()[0]

        # 2. 노드 저장
        node_id_map = {}
        for node in nodes:
            result = conn.execute(
                text("INSERT INTO nodes (snapshot_id, label) VALUES (:snapshot_id, :label) RETURNING id"),
                {"snapshot_id": snapshot_id, "label": node["label"]}
            )
            node_id_map[node["id"]] = result.fetchone()[0]

            # 3. 기사 저장
            for article in node.get("articles", []):
                conn.execute(
                    text("INSERT INTO articles (node_id, title, summary, date) VALUES (:node_id, :title, :summary, :date)"),
                    {"node_id": node_id_map[node["id"]], "title": article["title"], "summary": article["summary"], "date": article["date"]}
                )

        conn.commit()