from typing import Optional, List, Dict
from src.config.config import Config
from src.models.chatbot import BaseChatbot, OpenAIChatbot, OllamaChatbot

class ChatService:
    def __init__(self, config: Config):
        self.config = config
        self.default_system_message = "당신은 친절하고 도움이 되는 AI 어시스턴트입니다."
        self.chatbots: Dict[str, BaseChatbot] = {}
    
    def create_chatbot(self, model_type: str = "openai", system_message: Optional[str] = None) -> str:
        """새로운 챗봇 인스턴스를 생성합니다.

        Args:
            model_type: 사용할 모델 타입 ("openai" 또는 "ollama")
            system_message: 시스템 메시지 (없으면 기본값 사용)

        Returns:
            생성된 챗봇의 고유 ID
        """
        system_message = system_message or self.default_system_message
        
        if model_type == "openai":
            chatbot = OpenAIChatbot(self.config, system_message)
        elif model_type == "ollama":
            chatbot = OllamaChatbot(self.config, system_message)
        else:
            raise ValueError(f"지원하지 않는 모델 타입입니다: {model_type}")
        
        # 간단한 ID 생성 (실제로는 더 안전한 UUID 등을 사용해야 함)
        chat_id = f"{model_type}_{len(self.chatbots)}"
        self.chatbots[chat_id] = chatbot
        return chat_id
    
    def get_response(self, chat_id: str, message: str) -> str:
        """챗봇으로부터 응답을 받아옵니다.

        Args:
            chat_id: 챗봇 ID
            message: 사용자 메시지

        Returns:
            챗봇의 응답
        """
        if chat_id not in self.chatbots:
            raise ValueError(f"존재하지 않는 챗봇 ID입니다: {chat_id}")
        
        return self.chatbots[chat_id].get_response(message)
    
    def get_chat_history(self, chat_id: str) -> List[dict]:
        """채팅 기록을 가져옵니다.

        Args:
            chat_id: 챗봇 ID

        Returns:
            채팅 기록 리스트
        """
        if chat_id not in self.chatbots:
            raise ValueError(f"존재하지 않는 챗봇 ID입니다: {chat_id}")
        
        return self.chatbots[chat_id].get_chat_history()
