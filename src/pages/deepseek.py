"""
DeepSeek 모델 전용 페이지
"""
import streamlit as st
from src.components.sidebar import render_sidebar
from src.components.chat_interface import ChatInterface

def show():
    """DeepSeek 모델 페이지를 표시합니다."""
    st.title("🧠 DeepSeek AI와 대화하기")
    
    st.markdown("""
    ### DeepSeek AI 소개
    
    DeepSeek는 강력한 성능을 자랑하는 오픈소스 AI 모델입니다.
    다양한 주제에 대해 깊이 있는 대화가 가능합니다.
    
    #### 특징:
    - 코드 생성 및 분석
    - 기술적 문제 해결
    - 자연스러운 한국어 대화
    """)
    
    # 사이드바 표시
    render_sidebar()
    
    # 채팅 인터페이스 표시 (DeepSeek 모델 사용)
    chat_interface = ChatInterface("deepseek")
    chat_interface.render()
