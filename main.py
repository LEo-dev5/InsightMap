from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import summarizer
import crawler
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor
import db
from datetime import date

app = FastAPI()
cache = None
def refresh_cache():
    global cache
    cache = None
    get_nodes()

scheduler = BackgroundScheduler()
scheduler.add_job(refresh_cache, 'cron', hour=7, minute=0)
scheduler.start()

@app.get("/api/nodes")
def get_nodes():
    global cache
    if cache is not None:
        return cache
    
    articles = crawler.guardian_api_search()
    
    keyword_to_id = {}
    nodes = []
    edges = {}  # (from, to) → weight 딕셔너리

    with ThreadPoolExecutor(max_workers=2) as executor:
        summaries = list(executor.map(summarizer.summarize_article, articles))

    for result in summaries:
        keywords = result["keywords"]
        keyword_ids = []
        
        for keyword in keywords:
            if keyword not in keyword_to_id:
                new_id = len(nodes)
                keyword_to_id[keyword] = new_id
                nodes.append({
                    "id": new_id,
                    "label": keyword,
                    "articles": [],
                    "article_count": 0
                })
            keyword_ids.append(keyword_to_id[keyword])
            nodes[keyword_to_id[keyword]]["articles"].append({
                "title": result["title"],
                "summary": result["summary"],
                "date": result["date"],
                "url": result.get("url", "")
            })
            nodes[keyword_to_id[keyword]]["article_count"] += 1

        for i in range(len(keyword_ids)):
            for j in range(i + 1, len(keyword_ids)):
                key = (keyword_ids[i], keyword_ids[j])
                if key in edges:
                    edges[key] += 1
                else:
                    edges[key] = 1

    edges_list = [
        {"from": k[0], "to": k[1], "weight": v}
        for k, v in edges.items()
    ]

    db.save_snapshot(str(date.today()), nodes, edges_list)
    cache = {"nodes": nodes, "edges": edges_list}
    return cache

@app.get("/api/snapshot")
def get_snapshot(date: str):
    data = db.load_snapshot(date)
    if data is None:
        return {"error": "No snapshot found for this date"}
    return data

@app.get("/api/dates")
def get_dates():
    from sqlalchemy import text
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT date FROM snapshots ORDER BY date DESC"))
        return [str(row[0]) for row in result]

from fastapi.responses import FileResponse

@app.get("/")
def read_index():
    return FileResponse("static/index.html")