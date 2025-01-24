from src.config.config import Config
from src.models.chatbot import OpenAIChatbot, OllamaChatbot

def test_chatbots():
    config = Config.load_config()
    
    # OpenAI 챗봇 테스트
    openai_bot = OpenAIChatbot(config, "당신은 친절한 AI 어시스턴트입니다.")
    response = openai_bot.get_response("안녕하세요!")
    print("OpenAI 응답:", response)
    
    # Ollama 챗봇 테스트
    ollama_bot = OllamaChatbot(config, "당신은 친절한 AI 어시스턴트입니다.")
    response = ollama_bot.get_response("안녕하세요!")
    print("Ollama 응답:", response)

if __name__ == "__main__":
    test_chatbots()
