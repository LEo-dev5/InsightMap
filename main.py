from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import summarizer
import crawler

app = FastAPI()

@app.get("/api/nodes")
def get_nodes():
    articles = crawler.guardian_api_search()
    nodes = []
    for article in articles:
        result = summarizer.summarize_article(article)
        nodes.append(result)
    return nodes

from fastapi.responses import FileResponse

@app.get("/")
def read_index():
    return FileResponse("static/index.html")