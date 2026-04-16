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
                        text("INSERT INTO articles (title, summary, date, url) VALUES (:title, :summary, :date, :url) RETURNING id"),
                        {"title": title, "summary": article["summary"], "date": article["date"], "url": article.get("url", "")}
                    )
                    article_id_map[title] = result.fetchone()[0]

        # 3. 노드 저장 + node_articles 연결
        node_id_map = {}  # 파이썬 id → DB id 매핑
        for node in nodes:
            result = conn.execute(
                text("INSERT INTO nodes (snapshot_id, label) VALUES (:snapshot_id, :label) RETURNING id"),
                {"snapshot_id": snapshot_id, "label": node["label"]}
            )
            node_db_id = result.fetchone()[0]
            node_id_map[node["id"]] = node_db_id  # 매핑 저장

            for article in node.get("articles", []):
                article_id = article_id_map[article["title"]]
                conn.execute(
                    text("INSERT INTO node_articles (node_id, article_id) VALUES (:node_id, :article_id) ON CONFLICT DO NOTHING"),
                    {"node_id": node_db_id, "article_id": article_id}
                )

        # 4. 엣지 저장
        for edge in edges:
            from_db_id = node_id_map.get(edge["from"])
            to_db_id = node_id_map.get(edge["to"])
            if from_db_id and to_db_id:
                conn.execute(
                    text("INSERT INTO edges (snapshot_id, from_node, to_node, weight) VALUES (:snapshot_id, :from_node, :to_node, :weight)"),
                    {"snapshot_id": snapshot_id, "from_node": from_db_id, "to_node": to_db_id, "weight": edge.get("weight", 1)}
                )

        conn.commit()

def load_snapshot(date):
    with engine.connect() as conn:
        # 1. 날짜로 snapshot_id 찾기
        result = conn.execute(
            text("SELECT id FROM snapshots WHERE date = :date"),
            {"date": date}
        )
        row = result.fetchone()
        if row is None:
            return None
        snapshot_id = row[0]

        # 2. 노드 + 기사 한 번에 조회
        result = conn.execute(
            text("""
                SELECT n.id, n.label, a.title, a.summary, a.date, a.url
                FROM nodes n
                LEFT JOIN node_articles na ON n.id = na.node_id
                LEFT JOIN articles a ON na.article_id = a.id
                WHERE n.snapshot_id = :snapshot_id
                ORDER BY n.id
            """),
            {"snapshot_id": snapshot_id}
        )
        nodes_map = {}
        for row in result:
            node_id, label, title, summary, date, url = row
            if node_id not in nodes_map:
                nodes_map[node_id] = {"id": node_id, "label": label, "articles": [], "article_count": 0}
            if title:
                nodes_map[node_id]["articles"].append(
                    {"title": title, "summary": summary, "date": str(date), "url": url or ""}
                )
                nodes_map[node_id]["article_count"] += 1
        nodes = list(nodes_map.values())

        # 3. 엣지 조회
        result = conn.execute(
            text("SELECT from_node, to_node, weight FROM edges WHERE snapshot_id = :snapshot_id"),
            {"snapshot_id": snapshot_id}
        )
        edges = [{"from": row[0], "to": row[1], "weight": row[2]} for row in result]

        return {"nodes": nodes, "edges": edges}