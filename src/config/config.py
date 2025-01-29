from dataclasses import dataclass
from typing import Dict, Optional
import os
from dotenv import load_dotenv

@dataclass
class ModelConfig:
    """AI 모델의 설정을 정의하는 클래스

    Attributes:
        name (str): 모델의 이름 (예: "llama2", "mistral" 등)
        description (str): 모델에 대한 설명
        system_message (str): 모델의 기본 시스템 메시지
        temperature (float): 모델의 temperature 값 (0~1). 높을수록 더 창의적인 응답
        max_tokens (int): 생성할 최대 토큰 수
    """
    name: str
    description: str
    system_message: str
    temperature: float
    max_tokens: int

@dataclass
class Config:
    """애플리케이션의 전체 설정을 관리하는 클래스

    이 클래스는 Singleton 패턴을 사용하여 애플리케이션 전체에서 하나의 설정 인스턴스만 유지합니다.

    Attributes:
        openai_api_key (Optional[str]): OpenAI API 키 (현재는 사용하지 않음)
        ollama_base_url (str): Ollama 서버의 기본 URL
        available_models (Dict[str, ModelConfig]): 사용 가능한 모델들의 설정
    """
    openai_api_key: Optional[str]
    ollama_base_url: str
    available_models: Dict[str, ModelConfig]

    _instance = None

    @classmethod
    def load_config(cls) -> 'Config':
        """설정을 로드하고 Config 인스턴스를 반환합니다.

        Singleton 패턴을 사용하여 항상 동일한 설정 인스턴스를 반환합니다.

        Returns:
            Config: 설정 인스턴스
        """
        if cls._instance is None:
            # 기본 시스템 메시지 설정
            default_system_message = """당신은 도움이 되는 AI 어시스턴트입니다.
            사용자의 질문에 한국어로 친절하게 답변해 주세요.
            전문적인 내용은 정확하게 설명하고, 모르는 내용은 모른다고 솔직하게 답변하세요."""

            # 환경변수 로드
            load_dotenv()

            # 설정 인스턴스 생성
            cls._instance = cls(
                openai_api_key=os.getenv('OPENAI_API_KEY'),
                ollama_base_url="http://localhost:11434",
                available_models={
                    "llama2": ModelConfig(
                        name="llama2",
                        description="Meta의 Llama2 모델입니다. 일반적인 대화와 작업에 적합합니다.",
                        system_message=default_system_message,
                        temperature=0.7,
                        max_tokens=1000
                    ),
                    "llama3.2": ModelConfig(
                        name="llama3.2",
                        description="Meta의 최신 Llama 3.2 모델입니다. 더 강력한 성능과 자연스러운 대화가 가능합니다.",
                        system_message=default_system_message,
                        temperature=0.7,
                        max_tokens=1000
                    ),
                    "mistral": ModelConfig(
                        name="mistral",
                        description="Mistral AI의 오픈소스 모델입니다. 강력한 성능을 제공합니다.",
                        system_message=default_system_message,
                        temperature=0.7,
                        max_tokens=1000
                    ),
                    "neural-chat": ModelConfig(
                        name="neural-chat",
                        description="Intel의 Neural Chat 모델입니다. 자연스러운 대화에 특화되어 있습니다.",
                        system_message=default_system_message,
                        temperature=0.7,
                        max_tokens=1000
                    )
                }
            )
        return cls._instance
