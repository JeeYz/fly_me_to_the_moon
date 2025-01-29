from abc import ABC, abstractmethod
from typing import List, Optional
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from src.config.config import Config, ModelConfig

class BaseChatbot(ABC):
    """챗봇의 기본 인터페이스를 정의하는 추상 클래스

    이 클래스는 모든 챗봇 구현체가 따라야 하는 기본 인터페이스를 정의합니다.
    새로운 챗봇 유형을 추가할 때는 이 클래스를 상속받아 구현하면 됩니다.
    """

    @abstractmethod
    def get_response(self, message: str) -> str:
        """사용자 메시지에 대한 응답을 생성합니다.

        Args:
            message (str): 사용자가 입력한 메시지

        Returns:
            str: AI의 응답 메시지
        """
        pass

    @abstractmethod
    def get_chat_history(self) -> List[dict]:
        """현재까지의 대화 기록을 반환합니다.

        Returns:
            List[dict]: 대화 기록 목록. 각 항목은 'role'과 'content' 키를 가집니다.
        """
        pass

class OllamaChatbot(BaseChatbot):
    """Ollama 기반의 챗봇 구현체

    이 클래스는 Ollama를 사용하여 AI 챗봇을 구현합니다.
    LangChain의 ChatOllama를 사용하여 대화를 처리합니다.

    Attributes:
        config (Config): 전체 애플리케이션 설정
        model_config (ModelConfig): 현재 사용 중인 모델의 설정
        chat_history (List): 대화 기록을 저장하는 리스트
        llm (ChatOllama): LangChain의 ChatOllama 인스턴스
    """

    def __init__(self, config: Config, model_config: ModelConfig):
        """OllamaChatbot 인스턴스를 초기화합니다.

        Args:
            config (Config): 전체 애플리케이션 설정
            model_config (ModelConfig): 사용할 모델의 설정
        """
        self.config = config
        self.model_config = model_config
        self.chat_history: List = []

        # Ollama 모델 초기화
        self.llm = ChatOllama(
            base_url=config.ollama_base_url,
            model=model_config.name,
            temperature=model_config.temperature
        )

        # 시스템 메시지 추가
        if model_config.system_message:
            self.chat_history.append(
                SystemMessage(content=model_config.system_message)
            )

    def get_response(self, message: str) -> str:
        """사용자 메시지에 대한 응답을 생성합니다.

        Args:
            message (str): 사용자가 입력한 메시지

        Returns:
            str: AI의 응답 메시지

        Note:
            이 메서드는 다음과 같은 순서로 동작합니다:
            1. 사용자 메시지를 대화 기록에 추가
            2. LLM을 사용하여 응답 생성
            3. AI 응답을 대화 기록에 추가
            4. 응답 반환
        """
        # 사용자 메시지를 대화 기록에 추가
        user_message = HumanMessage(content=message)
        self.chat_history.append(user_message)

        # LLM을 사용하여 응답 생성
        response = self.llm.invoke(self.chat_history)

        # AI 응답을 대화 기록에 추가
        self.chat_history.append(response)

        return response.content

    def get_chat_history(self) -> List[dict]:
        """현재까지의 대화 기록을 반환합니다.

        Returns:
            List[dict]: 대화 기록 목록. 각 항목은 다음 형식을 가집니다:
                {
                    'role': str ('system', 'user', 또는 'assistant'),
                    'content': str (메시지 내용)
                }
        """
        history = []
        for message in self.chat_history:
            if isinstance(message, SystemMessage):
                role = "system"
            elif isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            else:
                continue

            history.append({
                "role": role,
                "content": message.content
            })
        return history
