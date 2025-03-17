# utils.py
# LangChain과 LangGraph에서 사용할 유틸리티 함수들

import os
import glob
import logging
from typing import List, Any, Union

# LangChain 관련 임포트
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.document_loaders import PyMuPDFLoader


# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




def format_chat_history(messages: List[Union[HumanMessage, AIMessage, SystemMessage]]) -> str:
    """
    메시지 목록을 문자열 형식으로 변환합니다.
    
    Args:
        messages (List[Union[HumanMessage, AIMessage, SystemMessage]]): 메시지 목록
        
    Returns:
        str: 포맷된 대화 내역
    """
    formatted_history = ""
    
    for message in messages:
        if isinstance(message, HumanMessage):
            formatted_history += f"Human: {message.content}\n"
        elif isinstance(message, AIMessage):
            formatted_history += f"AI: {message.content}\n"
        elif isinstance(message, SystemMessage):
            formatted_history += f"System: {message.content}\n"
    
    return formatted_history
