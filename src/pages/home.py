"""
메인 홈 페이지 모듈
"""
import streamlit as st
from src.components.sidebar import render_sidebar

def show():
    """메인 홈 페이지를 표시합니다."""
    st.title("🚀 Fly me to the Moon - AI 챗봇")
    
    st.markdown("""
    ### 환영합니다! 👋
    
    AI 챗봇과 대화를 시작해보세요.
    
    #### 사용 가능한 챗봇:
    
    ##### 🧠 DeepSeek
    - 코드 생성 및 분석
    - 기술적 문제 해결
    - 자연스러운 한국어 대화
    
    ##### 🎯 Claude
    - 정확하고 신뢰성 있는 정보 제공
    - 윤리적이고 안전한 응답
    - 복잡한 작업 수행 능력
    
    왼쪽 사이드바에서 원하시는 챗봇을 선택하고 대화를 시작하세요!
    """)
    
    # 사이드바 표시
    render_sidebar()
