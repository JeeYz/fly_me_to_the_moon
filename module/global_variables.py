import os
import logging

# 로거 설정
# 현재 모듈의 로거 생성 및 로깅 레벨 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#################################################
# 경로 설정
#################################################

# PDF 문서 타겟 폴더 경로 설정
pdf_path = "../무역보험영업봇_근거자료/"

# 절대 경로로 변환
absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), pdf_path))

# 벡터 저장소 경로 설정
vector_store_path = "./cache"
# 벡터 저장소 절대 경로 변환
absolute_vector_store_path = os.path.abspath(os.path.join(os.path.dirname(__file__), vector_store_path))

#################################################
# 모델 설정
#################################################

# 기본 모델 종류 설정
model_type = "ollama"

# Ollama 모델 목록
ollama_models = [
    "llama3.1",
    "mistral",
    "gemma2:9b",
    "phi4",
    "olmo2:13b",
    "command-r7b",
]

# Ollama 임베딩 모델 목록
ollama_embedding_models = [
    "granite-embedding:278m",
    "snowflake-arctic-embed2",
    "nomic-embed-text:latest"
]

# HuggingFace 모델 목록
hf_models = [
    "mistralai/Mistral-7B-Instruct-v0.2",
    "meta-llama/Llama-2-7b-chat-hf",
    "google/gemma-7b",
    "microsoft/phi-2",
    "HuggingFaceH4/zephyr-7b-beta"
]

