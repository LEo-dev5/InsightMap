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
    edges = []

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
                    "articles": []
                })
            keyword_ids.append(keyword_to_id[keyword])
            nodes[keyword_to_id[keyword]]["articles"].append({
                "title": result["title"],
                "summary": result["summary"],
                "date": result["date"],
                "url": result.get("url", "")
            })

        for i in range(len(keyword_ids)):
            for j in range(i + 1, len(keyword_ids)):
                edges.append({"from": keyword_ids[i], "to": keyword_ids[j]})

    db.save_snapshot(str(date.today()), nodes, edges)
    cache = {"nodes": nodes, "edges": edges}
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