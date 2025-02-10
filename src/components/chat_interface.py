"""
채팅 인터페이스 컴포넌트 모듈

이 모듈은 사용자와 AI 모델 간의 대화 인터페이스를 관리합니다.
대화 흐름:
1. 사용자가 메시지 입력
2. 메시지가 AI 모델로 전달
3. AI 모델이 응답 생성
4. 응답이 화면에 표시
"""
import streamlit as st
from src.config.config import Config
from src.services.chat_service import ChatService

class ChatInterface:
    """채팅 인터페이스를 관리하는 클래스
    
    이 클래스는 다음과 같은 기능을 담당합니다:
    - 채팅 UI 렌더링
    - 사용자 입력 처리
    - AI 응답 처리
    - 대화 기록 관리
    """
    
    def __init__(self, model_name):
        """ChatInterface 인스턴스를 초기화합니다.
        
        Args:
            model_name (str): 사용할 AI 모델의 이름
        
        Config와 ChatService 인스턴스를 생성하고,
        세션 상태를 초기화합니다.
        """
        self.config = Config.load_config()
        self.chat_service = ChatService(self.config)
        self.model_name = model_name
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """세션 상태를 초기화합니다.
        
        초기화되는 항목:
        - messages: 대화 기록을 저장하는 리스트
        - chat_id: 현재 대화 세션의 ID
        
        각 메시지는 다음 형식의 딕셔너리입니다:
        {
            "role": "user" 또는 "assistant",
            "content": "메시지 내용"
        }
        """
        # 페이지별로 독립적인 대화 기록을 유지하기 위해 
        # 모델 이름을 포함한 키를 사용
        messages_key = f"messages_{self.model_name}"
        chat_id_key = f"chat_id_{self.model_name}"
        
        if messages_key not in st.session_state:
            st.session_state[messages_key] = []
        if chat_id_key not in st.session_state:
            st.session_state[chat_id_key] = self.chat_service.create_chatbot(self.model_name)
    
    def _get_messages_key(self):
        """현재 모델의 메시지 키를 반환합니다."""
        return f"messages_{self.model_name}"
    
    def _get_chat_id_key(self):
        """현재 모델의 채팅 ID 키를 반환합니다."""
        return f"chat_id_{self.model_name}"
    
    def _display_message(self, message):
        """메시지를 화면에 표시합니다.
        
        Args:
            message (dict): 표시할 메시지 딕셔너리
                - role: 메시지 작성자 ("user" 또는 "assistant")
                - content: 메시지 내용
        """
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    def render(self):
        """채팅 인터페이스를 렌더링합니다.
        
        대화 흐름:
        1. 이전 대화 기록 표시
        2. 사용자 입력 받기
        3. 입력된 메시지 처리:
            a. 사용자 메시지를 대화 기록에 추가
            b. AI 모델에 메시지 전달
            c. AI 응답을 대화 기록에 추가
            d. 화면 업데이트
        """
        messages_key = self._get_messages_key()
        chat_id_key = self._get_chat_id_key()
        
        # 이전 메시지들 표시
        for message in st.session_state[messages_key]:
            self._display_message(message)
        
        # 사용자 입력 처리
        # streamlit의 chat_input을 통해 사용자 입력을 받음
        if prompt := st.chat_input("메시지를 입력하세요"):
            # 사용자 메시지를 대화 기록에 추가
            user_message = {"role": "user", "content": prompt}
            st.session_state[messages_key].append(user_message)
            self._display_message(user_message)
            
            # AI 응답 생성
            # 1. chat_service를 통해 현재 모델에 메시지 전달
            # 2. 모델이 응답을 생성할 때까지 대기 (스피너 표시)
            with st.spinner("AI가 응답을 생성중입니다..."):
                response = self.chat_service.get_response(
                    st.session_state[chat_id_key],  # 현재 대화 세션 ID
                    prompt  # 사용자 입력 메시지
                )
            
            # AI 응답을 대화 기록에 추가하고 화면에 표시
            ai_message = {"role": "assistant", "content": response}
            st.session_state[messages_key].append(ai_message)
            self._display_message(ai_message)
