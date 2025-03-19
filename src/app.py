import os
import streamlit as st
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, AIMessage

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="Ollama 챗봇",
    page_icon="🤖",
    layout="wide"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm_model" not in st.session_state:
    st.session_state.llm_model = "gemma3:4b"

# 사이드바 설정
with st.sidebar:
    st.title("🤖 LLM 챗봇 설정")
    
    # 모델 선택
    st.subheader("모델 설정")
    model_option = st.selectbox(
        "사용할 LLM 모델을 선택하세요:",
        options=[
            "gemma3:4b",
            "llama3.2:3b", 
            "llama3.1", 
        ],
        index=0
    )
    
    # 모델 파라미터 설정
    st.subheader("모델 파라미터")
    temperature = st.slider(
        "Temperature", 
        min_value=0.0, 
        max_value=2.0, 
        value=0.7, 
        step=0.1
    )

    max_tokens = st.slider(
        "최대 토큰 수", 
        min_value=100, 
        max_value=4000, 
        value=1000, 
        step=100
    )
    
    # 모델 적용 버튼
    if st.button("설정 적용"):
        st.session_state.llm_model = model_option
        st.success(f"모델이 {model_option}로 변경되었습니다!")
    
    # 대화 초기화 버튼
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.success("대화가 초기화되었습니다!")
    
    st.divider()
    st.caption("© 2025 LLM 챗봇 | 모든 권리 보유")

# 메인 화면 설정
st.title("🤖 LLM 챗봇")
st.subheader(f"현재 모델: {st.session_state.llm_model}")

# 이전 대화 내용 표시
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    else:  # AIMessage
        with st.chat_message("assistant"):
            st.write(message.content)

# 사용자 입력 처리
if prompt := st.chat_input("무엇이든 물어보세요!"):
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.write(prompt)
    
    # AI 응답 생성 중 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("생각 중...")
        
        try:
            # LLM 모델 초기화
            llm = ChatOllama(
                model=st.session_state.llm_model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # 응답 생성
            response = llm.invoke(st.session_state.messages)
            
            # 응답 표시
            message_placeholder.markdown(response.content)
            
            # 응답 저장
            st.session_state.messages.append(AIMessage(content=response.content))
            
        except Exception as e:
            message_placeholder.markdown(f"오류가 발생했습니다: {str(e)}")

# 앱 실행 방법 안내
st.sidebar.markdown("""\n### 실행 방법\n```bash\nstreamlit run app.py\n```""")
