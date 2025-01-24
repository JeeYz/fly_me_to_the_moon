import os
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Optional

@dataclass
class LLMConfig:
    model_name: str
    temperature: float
    max_tokens: int

@dataclass
class Config:
    openai_api_key: Optional[str]
    openai_config: LLMConfig
    ollama_base_url: str
    ollama_config: LLMConfig

    @classmethod
    def load_config(cls) -> 'Config':
        load_dotenv()
        
        return cls(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            openai_config=LLMConfig(
                model_name="gpt-3.5-turbo",
                temperature=0.7,
                max_tokens=1000
            ),
            ollama_base_url="http://localhost:11434",
            ollama_config=LLMConfig(
                model_name="llama2",
                temperature=0.7,
                max_tokens=1000
            )
        )
