import os
from dotenv import load_dotenv
import requests

load_dotenv()

def guardian_api_search():
    api_key = os.getenv('GUARDIAN_API_KEY')
    
    if not api_key:
        raise ValueError("GUARDIAN_API_KEY가 설정되지 않았어요")

    url = "https://content.guardianapis.com/search"

    params = {
        "q": "defense OR military OR war",
        "section": "world",
        "show-fields": "bodyText",
        "page-size": 20,
        "api-key": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        raise Exception("Guardian API 요청 시간이 초과됐어요")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Guardian API 요청 실패: {e}")

    articles = []
    for article in data["response"]["results"]:
        try:
            articles.append({
                "text": article["fields"]["bodyText"],
                "date": article["webPublicationDate"][:10],
                "url": article["webUrl"]
            })
        except KeyError:
            continue  # bodyText 없는 기사는 건너뜀

    return articles