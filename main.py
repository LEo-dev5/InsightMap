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

    edges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            keywords_i = set(nodes[i]["keywords"])
            keywords_j = set(nodes[j]["keywords"])
            if keywords_i & keywords_j:
                edges.append({"from": i, "to": j})

    return {"nodes": nodes, "edges": edges}

from fastapi.responses import FileResponse

@app.get("/")
def read_index():
    return FileResponse("static/index.html")