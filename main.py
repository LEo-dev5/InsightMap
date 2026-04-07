from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import summarizer
import crawler
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor

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

    with ThreadPoolExecutor(max_workers=3) as executor:
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
                "summary": result["summary"]
            })

        for i in range(len(keyword_ids)):
            for j in range(i + 1, len(keyword_ids)):
                edges.append({"from": keyword_ids[i], "to": keyword_ids[j]})

    cache = {"nodes": nodes, "edges": edges}
    return cache

from fastapi.responses import FileResponse

@app.get("/")
def read_index():
    return FileResponse("static/index.html")