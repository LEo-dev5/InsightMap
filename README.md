# 🗺️ InsightMap

> 글로벌 뉴스를 AI가 키워드로 분석해 옵시디언 스타일 그래프로 시각화하는 지정학 인사이트 도구

![Python](https://img.shields.io/badge/Python-3.9-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Claude API](https://img.shields.io/badge/Claude-Haiku-orange)
![vis.js](https://img.shields.io/badge/vis.js-network-purple)

---

## 💡 왜 만들었나요?

매일 아침 뉴스를 보면서 이런 생각을 했습니다.

> *"자원 제한 하나가 어떤 산업을 흔드는지, 그 연결고리를 한눈에 볼 수 있으면 어떨까?"*

같은 뉴스를 봐도 이런 연결고리를 찾아내는 사람들이 있습니다.  
InsightMap은 그 과정을 시각화해줍니다.

Guardian API로 실시간 글로벌 뉴스를 가져오고, Claude AI가 핵심 키워드를 추출한 뒤,  
공통 키워드끼리 노드를 연결해 **한눈에 뉴스 간 연관성을 파악**할 수 있습니다.

---

## ✨ 주요 기능

- 🌍 **실시간 글로벌 뉴스 수집** — Guardian API로 방산/지정학 뉴스 자동 수집
- 🤖 **AI 키워드 추출** — Claude Haiku가 각 기사에서 핵심 키워드 추출
- 🕸️ **옵시디언 스타일 그래프** — 공통 키워드를 가진 뉴스끼리 노드로 연결
- 🖱️ **인터랙티브 시각화** — 노드 클릭 시 관련 기사 요약 사이드패널 표시
- ⚡ **병렬 처리** — ThreadPoolExecutor로 다수 기사 동시 분석
- 🕐 **자동 캐싱 & 갱신** — 매일 오전 7시 자동으로 최신 뉴스로 갱신

---

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| Backend | Python, FastAPI |
| AI | Claude API (Haiku) |
| News | Guardian API |
| Frontend | HTML, CSS, JavaScript |
| Visualization | vis-network.js |
| Scheduling | APScheduler |

---

## 🚀 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/LEo-dev5/InsightMap.git
cd InsightMap
```

### 2. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate  # macOS
```

### 3. 패키지 설치
```bash
pip install fastapi uvicorn anthropic newspaper3k \
            lxml_html_clean python-dotenv newsapi-python \
            apscheduler requests beautifulsoup4
```

### 4. 환경변수 설정
`.env` 파일을 생성하고 아래 내용을 입력하세요:
```
GUARDIAN_API_KEY=your_guardian_api_key
CLAUDE_API_KEY=your_claude_api_key
```

- Guardian API 키 발급: https://open-platform.theguardian.com/
- Claude API 키 발급: https://console.anthropic.com/

### 5. 서버 실행
```bash
uvicorn main:app
```

브라우저에서 `http://localhost:8000` 접속

---

## 📁 프로젝트 구조

```
InsightMap/
├── main.py          # FastAPI 서버, 노드/엣지 생성 로직
├── crawler.py       # Guardian API 뉴스 수집
├── summarizer.py    # Claude API 키워드 추출
├── static/
│   └── index.html   # vis.js 그래프 시각화
└── .env             # API 키 (깃허브 업로드 금지)
```

---

## 🔮 앞으로 추가할 기능

- [ ] 날짜별 그래프 저장 및 비교 (DB 연동)
- [ ] 유튜브 링크 입력 → 자막 추출 → 노드 생성
- [ ] 키워드 필터링 및 검색
- [ ] 뉴스 분야 커스터마이징

---

## 📝 개발 과정에서 배운 것

- Guardian API, Claude API 연동
- FastAPI로 백엔드 API 설계
- ThreadPoolExecutor를 활용한 병렬 처리
- vis-network.js로 인터랙티브 그래프 구현
- 캐싱으로 API 비용 최적화

---

> 개발자: [강용원](https://github.com/LEo-dev5)  
> 블로그: [leo-dev5.github.io](https://leo-dev5.github.io)
