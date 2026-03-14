import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv('GUARDIAN_API_KEY')

url = "http://content.guardianapis.com/search"

params = {
    "q": "defense",
    "show-fields" : "bodyText",
    "page-size" : 3,
    "api-key": api_key
}

response = requests.get(url,  params=params)
data = response.json()

for article in data["response"]["results"]:
    print(article["webTitle"])
    print(article["fields"]["bodyText"][:200])
    print()