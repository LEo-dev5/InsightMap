import os
from dotenv import load_dotenv
import anthropic
import json
import crawler

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def summarize_article(text):
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

기사:
{text}"""
            }
        ]
    )
    raw = message.content[0].text
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)

articles = crawler.guardian_api_search()
for article in articles:
    result = summarize_article(article)
    print(result)