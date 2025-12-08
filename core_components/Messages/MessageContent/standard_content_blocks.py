# Message具有一个content属性,该属性是弱类型的，支持字符串和未类型化对象（例如字典）的列表。
# 这使得langchain聊天模型能够直接支持模型提供商的原生结构，例如多模块内容及其他数据。

from langchain.messages import HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv  
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")
# String content
human_message = HumanMessage("Hello, how are you?")

# Provider-native format (e.g., OpenAI)
human_message = HumanMessage(content=[
    {"type": "text", "text": "Hello, how are you?"},
    {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
])

# List of standard content blocks
human_message = HumanMessage(content_blocks=[
    {"type": "text", "text": "Hello, how are you?"},
    {"type": "image", "url": "https://example.com/image.jpg"},
])

model = init_chat_model(
    model = "gpt-5",
    base_url = "http://localhost:8317/v1",
    reasoning = {
        "effort": "medium",
        "summary" : "auto"
    },
    # output_version = "v1"  # Ensure the model returns standard content
)
response = model.invoke("一块巧克力重240g,如果我每天吃一半，多少天后我会吃完？")
print(response.content)  # List of standard content in the response