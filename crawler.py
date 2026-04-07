import os
from dotenv import load_dotenv
import requests

load_dotenv()

def guardian_api_search():
    api_key = os.getenv('GUARDIAN_API_KEY')

    url = "http://content.guardianapis.com/search"

    params = {
    "q": "defense OR military OR war",
    "section": "world",
    "show-fields": "bodyText",
    "page-size": 20,
    "api-key": api_key
}
    response = requests.get(url,  params=params)  #api get 요청  -> url에서 params 형식으로 
    data = response.json()      #json 형식으로 파싱

    articles = [] #빈 리스트 생성

    for article in data["response"]["results"]:             
        articles.append(article["fields"]["bodyText"])

    return articles
