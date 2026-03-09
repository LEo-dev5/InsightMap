from newspaper import Article
url = "https://n.news.naver.com/article/001/0015077942"

article = Article(url, language='ko')
article.download()
article.parse()
print(article.text)