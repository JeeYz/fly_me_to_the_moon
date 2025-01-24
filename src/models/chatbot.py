from typing import List, Optional
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_community.llms import Ollama

from src.config.config import Config, LLMConfig

class BaseChatbot:
    def __init__(self, system_message: str):
        self.messages: List[BaseMessage] = [
            SystemMessage(content=system_message)
        ]
    
    def add_message(self, content: str, role: str = "human") -> None:
        if role == "human":
            self.messages.append(HumanMessage(content=content))
        elif role == "ai":
            self.messages.append(AIMessage(content=content))
    
    def get_chat_history(self) -> List[dict]:
        return [
            {"role": "system" if isinstance(msg, SystemMessage)
                     else "user" if isinstance(msg, HumanMessage)
                     else "assistant",
             "content": msg.content}
            for msg in self.messages
        ]

class OpenAIChatbot(BaseChatbot):
    def __init__(self, config: Config, system_message: str):
        super().__init__(system_message)
        self.chat_model = ChatOpenAI(
            openai_api_key=config.openai_api_key,
            model_name=config.openai_config.model_name,
            temperature=config.openai_config.temperature
        )
    
    def get_response(self, message: str) -> str:
        self.add_message(message)
        response = self.chat_model.invoke(self.messages)
        self.add_message(response.content, role="ai")
        return response.content

class OllamaChatbot(BaseChatbot):
    def __init__(self, config: Config, system_message: str):
        super().__init__(system_message)
        self.chat_model = Ollama(
            base_url=config.ollama_base_url,
            model=config.ollama_config.model_name,
            temperature=config.ollama_config.temperature
        )
    
    def get_response(self, message: str) -> str:
        self.add_message(message)
        # Ollama에서는 전체 대화 내용을 문자열로 변환하여 전송
        chat_history = "\n".join([msg.content for msg in self.messages])
        response = self.chat_model.invoke(chat_history)
        self.add_message(response, role="ai")
        return response
