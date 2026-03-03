import requests
from bs4 import BeautifulSoup

url = "https://n.news.naver.com/article/001/0015077942"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

print(soup.get_text())
