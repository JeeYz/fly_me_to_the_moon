import streamlit as st
from src.services.chat_service import ChatService

class ChatbotApp:
    def __init__(self):
        self.chat_service = ChatService()
        
    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def display_chat_history(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def run(self):
        st.title("🤖 AI 챗봇")
        st.markdown("""
        안녕하세요! 저는 당신의 AI 어시스턴트입니다.
        무엇을 도와드릴까요?
        """)

        # 세션 상태 초기화
        self.initialize_session_state()
        
        # 채팅 히스토리 표시
        self.display_chat_history()

        # 사용자 입력 처리
        if prompt := st.chat_input("메시지를 입력하세요..."):
            # 사용자 메시지 추가
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # AI 응답 생성
            with st.chat_message("assistant"):
                with st.spinner("생각 중..."):
                    response = self.chat_service.get_response(prompt)
                    st.markdown(response)
            
            # AI 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    app = ChatbotApp()
    app.run()
