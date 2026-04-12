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

        # 2. 기사 중복 제거 (title 기준)
        article_id_map = {}
        for node in nodes:
            for article in node.get("articles", []):
                title = article["title"]
                if title not in article_id_map:
                    result = conn.execute(
                        text("INSERT INTO articles (title, summary, date) VALUES (:title, :summary, :date) RETURNING id"),
                        {"title": title, "summary": article["summary"], "date": article["date"]}
                    )
                    article_id_map[title] = result.fetchone()[0]

        # 3. 노드 저장 + node_articles 연결
        for node in nodes:
            result = conn.execute(
                text("INSERT INTO nodes (snapshot_id, label) VALUES (:snapshot_id, :label) RETURNING id"),
                {"snapshot_id": snapshot_id, "label": node["label"]}
            )
            node_db_id = result.fetchone()[0]

            for article in node.get("articles", []):
                article_id = article_id_map[article["title"]]
                conn.execute(
                    text("INSERT INTO node_articles (node_id, article_id) VALUES (:node_id, :article_id) ON CONFLICT DO NOTHING"),
                    {"node_id": node_db_id, "article_id": article_id}
                )

        conn.commit()