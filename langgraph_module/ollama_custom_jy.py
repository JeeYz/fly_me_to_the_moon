from typing import (
    List, 
    Optional, 
    Union, 
    Literal, 
    Annotated
)
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from langchain_ollama.chat_models import ChatOllama


class OllamaCustomJY():
    def __init__(
        self, 
        model_name: Literal[
            "gemma3:4b", 
            "llama3.2:3b", 
            "llama3.1"], 
        temperature: float, 
        max_tokens: int
    ) -> None:
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.llm = ChatOllama(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

    
    def invoke(self, messages):
        return self.llm.invoke(messages)

    def bind_tools(self, tools):
        self.tools = tools
        return self

