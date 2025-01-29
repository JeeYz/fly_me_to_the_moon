from typing import Dict, List
from src.config.config import Config
from src.models.chatbot import BaseChatbot, OllamaChatbot

class ChatService:
    """채팅 서비스를 관리하는 클래스

    이 클래스는 여러 챗봇 인스턴스를 관리하고, 사용자의 요청을 적절한 챗봇에 전달하는 역할을 합니다.
    각 모델별로 하나의 챗봇 인스턴스를 유지하며, 모델 전환 시 새로운 대화를 시작합니다.

    Attributes:
        config (Config): 애플리케이션 설정
        chatbots (Dict[str, BaseChatbot]): 현재 활성화된 챗봇들의 딕셔너리
    """

    def __init__(self, config: Config):
        """ChatService 인스턴스를 초기화합니다.

        Args:
            config (Config): 애플리케이션 설정
        """
        self.config = config
        self.chatbots: Dict[str, BaseChatbot] = {}
    
    def create_chatbot(self, model_name: str) -> str:
        """새로운 챗봇 인스턴스를 생성합니다.

        Args:
            model_name (str): 사용할 모델의 이름

        Returns:
            str: 생성된 챗봇의 ID (모델 이름과 동일)

        Raises:
            ValueError: 지원하지 않는 모델 이름이 주어진 경우
        """
        if model_name not in self.config.available_models:
            raise ValueError(f"지원하지 않는 모델입니다: {model_name}")
        
        model_config = self.config.available_models[model_name]
        chatbot = OllamaChatbot(self.config, model_config)
        
        # 모델 이름을 챗봇 ID로 사용
        self.chatbots[model_name] = chatbot
        return model_name
    
    def get_response(self, chat_id: str, message: str) -> str:
        """챗봇으로부터 응답을 받아옵니다.

        Args:
            chat_id (str): 챗봇 ID (모델 이름과 동일)
            message (str): 사용자 메시지

        Returns:
            str: 챗봇의 응답

        Note:
            챗봇이 존재하지 않는 경우 자동으로 새로 생성합니다.
        """
        if chat_id not in self.chatbots:
            # 챗봇이 없으면 새로 생성
            self.create_chatbot(chat_id)
        
        return self.chatbots[chat_id].get_response(message)
    
    def get_chat_history(self, chat_id: str) -> List[dict]:
        """채팅 기록을 가져옵니다.

        Args:
            chat_id (str): 챗봇 ID (모델 이름과 동일)

        Returns:
            List[dict]: 채팅 기록 목록

        Raises:
            ValueError: 존재하지 않는 챗봇 ID가 주어진 경우
        """
        if chat_id not in self.chatbots:
            raise ValueError(f"존재하지 않는 챗봇 ID입니다: {chat_id}")
        
        return self.chatbots[chat_id].get_chat_history()
    
    def get_available_models(self) -> Dict[str, str]:
        """사용 가능한 모델 목록을 가져옵니다.

        Returns:
            Dict[str, str]: 모델 이름과 설명을 담은 딕셔너리
        """
        return {
            name: config.description
            for name, config in self.config.available_models.items()
        }
