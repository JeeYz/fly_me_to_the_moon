# AI 챗봇 애플리케이션

Streamlit과 LangChain을 사용한 AI 챗봇 애플리케이션입니다.

## 설치 방법

1. Python 3.12 가상환경 생성 및 활성화:
```bash
python3.12 -m venv python3.12
source python3.12/bin/activate
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. `.env` 파일 설정:
- `.env` 파일을 열고 `OPENAI_API_KEY`에 실제 OpenAI API 키를 입력하세요.

## 실행 방법

```bash
streamlit run app.py
```

## 프로젝트 구조

```
.
├── src/
│   ├── config/
│   │   └── config.py
│   ├── models/
│   │   └── chatbot.py
│   └── services/
│       └── chat_service.py
├── .env
├── app.py
├── requirements.txt
└── README.md
```

## 주요 기능

- OpenAI GPT 모델을 사용한 대화형 챗봇
- 대화 히스토리 유지
- 사용자 친화적인 인터페이스
- 오류 처리 및 예외 상황 관리
