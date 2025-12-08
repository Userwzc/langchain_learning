from langchain.chat_models import init_chat_model
from dotenv import load_dotenv  
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

model  = init_chat_model(
    model = "gpt-5.1",
    base_url = "http://localhost:8317/v1"
)

# 你也可以直接使用 OpenAI 聊天补全格式指定消息。
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I'm fine, thank you! How can I assist you today?"}
]
response = model.invoke(messages)