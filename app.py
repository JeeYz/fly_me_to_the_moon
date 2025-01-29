import streamlit as st
from src.services.chat_service import ChatService
from src.config.config import Config

class ChatbotApp:
    """Streamlit 기반의 챗봇 웹 애플리케이션

    이 클래스는 웹 인터페이스를 통해 사용자와 AI 챗봇 간의 상호작용을 관리합니다.
    Streamlit의 세션 상태를 사용하여 대화 기록과 현재 선택된 모델을 유지합니다.

    Attributes:
        config (Config): 애플리케이션 설정
        chat_service (ChatService): 챗봇 서비스 인스턴스
    """

    def __init__(self):
        """ChatbotApp 인스턴스를 초기화합니다."""
        self.config = Config.load_config()
        self.chat_service = ChatService(self.config)
        
    def initialize_session_state(self):
        """Streamlit 세션 상태를 초기화합니다.

        다음 상태들을 초기화합니다:
        - messages: 대화 기록
        - current_model: 현재 선택된 모델
        - chat_id: 현재 활성화된 챗봇의 ID
        """
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "current_model" not in st.session_state:
            st.session_state.current_model = list(self.config.available_models.keys())[0]
        if "chat_id" not in st.session_state:
            st.session_state.chat_id = self.chat_service.create_chatbot(st.session_state.current_model)

    def display_sidebar(self):
        """사이드바를 표시합니다.

        사이드바에는 다음 요소들이 포함됩니다:
        - 모델 선택 라디오 버튼
        - 사용 방법 안내
        - 주의사항
        """
        st.sidebar.title("🤖 모델 선택")
        available_models = self.chat_service.get_available_models()
        
        selected_model = st.sidebar.radio(
            "대화할 AI 모델을 선택하세요:",
            options=list(available_models.keys()),
            format_func=lambda x: f"{x} - {available_models[x]}"
        )
        
        # 모델이 변경되면 새로운 대화 시작
        if selected_model != st.session_state.current_model:
            st.session_state.current_model = selected_model
            st.session_state.messages = []
            st.session_state.chat_id = self.chat_service.create_chatbot(selected_model)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        ### 사용 방법
        1. 원하는 AI 모델을 선택하세요
        2. 메시지를 입력하고 Enter를 누르세요
        3. AI의 응답을 기다리세요
        
        ### 주의사항
        - 모델을 변경하면 대화 내용이 초기화됩니다
        - 각 모델은 서로 다른 특성을 가지고 있습니다
        """)

    def display_chat_history(self):
        """채팅 기록을 화면에 표시합니다.

        st.session_state.messages에 저장된 모든 메시지를 순서대로 표시합니다.
        각 메시지는 발신자(사용자/AI)에 따라 다른 스타일로 표시됩니다.
        """
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def run(self):
        """애플리케이션을 실행합니다.

        다음 순서로 실행됩니다:
        1. 제목과 소개 표시
        2. 세션 상태 초기화
        3. 사이드바 표시
        4. 채팅 기록 표시
        5. 사용자 입력 처리
        """
        st.title("🤖 AI 챗봇")
        st.markdown("""
        안녕하세요! 저는 당신의 AI 어시스턴트입니다.
        무엇을 도와드릴까요?
        """)

        # 세션 상태 초기화
        self.initialize_session_state()
        
        # 사이드바 표시
        self.display_sidebar()
        
        # 채팅 기록 표시
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
                    response = self.chat_service.get_response(st.session_state.chat_id, prompt)
                    st.markdown(response)
            
            # AI 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    app = ChatbotApp()
    app.run()
