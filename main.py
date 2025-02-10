"""
메인 애플리케이션 모듈

이 모듈은 Streamlit 애플리케이션의 진입점입니다.
다음과 같은 기능을 제공합니다:
- 페이지 설정 및 초기화
- 페이지 라우팅
- 사용자 인터페이스 렌더링

애플리케이션 흐름:
1. 페이지 설정 초기화
2. 사용자가 사이드바에서 페이지 선택
3. 선택된 페이지의 show() 함수 호출
4. 페이지 컨텐츠 렌더링
"""
import streamlit as st
from src.pages import home, deepseek, claude

# 페이지 설정
# - page_title: 브라우저 탭에 표시될 제목
# - page_icon: 브라우저 탭에 표시될 아이콘
# - layout: 페이지 레이아웃 ("wide" = 전체 화면 너비 사용)
# - initial_sidebar_state: 사이드바 초기 상태
st.set_page_config(
    page_title="Fly me to the Moon - AI 챗봇",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 페이지 매핑
# 각 페이지 모듈과 해당 이름을 매핑
PAGES = {
    "Home": home,
    "DeepSeek 챗봇": deepseek,
    "Claude 챗봇": claude
}

def main():
    """메인 애플리케이션을 실행합니다.
    
    동작 순서:
    1. 사이드바에 페이지 선택 옵션 표시
    2. 사용자가 페이지 선택
    3. 선택된 페이지의 show() 함수 호출
    4. 페이지 컨텐츠 렌더링
    """
    # 페이지 선택
    # selectbox를 사용하여 사용자가 페이지를 선택할 수 있게 함
    page = st.sidebar.selectbox("AI 챗봇 선택", list(PAGES.keys()))
    
    # 선택된 페이지 표시
    # 해당 페이지 모듈의 show() 함수 호출
    PAGES[page].show()

if __name__ == "__main__":
    main()
