import os
from dotenv import load_dotenv
import anthropic
import json
import crawler
import time

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def summarize_article(article):
    time.sleep(0.5)  # 0.5초 대기
    text = article["text"]
    date = article["date"]
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""아래 기사를 분석해서 JSON 형식으로만 답해줘.
                다른 말은 절대 하지 말고 JSON만 출력해.

                {{
                "title": "한 줄 제목",
                "summary": "3줄 요약",
                "keywords": ["키워드1", "키워드2", "키워드3"]
                }}

                키워드 규칙:
                - 반드시 2-4글자의 짧고 일반적인 단어로
                - 띄어쓰기 없이 붙여서
                - 예시: "우크라이나전쟁", "NATO", "이란갈등", "방산"

                기사:
                {text}"""
            }
        ]
    )
    raw = message.content[0].text
    clean = raw.replace("```json", "").replace("```", "").strip()
    result = json.loads(clean)
    result["date"] = date
    return result

articles = crawler.guardian_api_search()
for article in articles:
    result = summarize_article(article)
    print(result)