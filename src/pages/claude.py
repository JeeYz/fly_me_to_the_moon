"""
Claude 모델 전용 페이지
"""
import streamlit as st
from src.components.sidebar import render_sidebar
from src.components.chat_interface import ChatInterface

def show():
    """Claude 모델 페이지를 표시합니다."""
    st.title("🎯 Claude AI와 대화하기")
    
    st.markdown("""
    ### Claude AI 소개
    
    Claude는 Anthropic에서 개발한 고성능 AI 어시스턴트입니다.
    안전하고 유용한 대화를 제공합니다.
    
    #### 특징:
    - 정확하고 신뢰성 있는 정보 제공
    - 윤리적이고 안전한 응답
    - 복잡한 작업 수행 능력
    """)
    
    # 사이드바 표시
    render_sidebar()
    
    # 채팅 인터페이스 표시 (Claude 모델 사용)
    chat_interface = ChatInterface("claude")
    chat_interface.render()
