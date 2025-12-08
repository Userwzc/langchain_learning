# Human message : Represents user input and interactions with the model.
# HumanMessage 代表用户输入和交互。它们可以包含文本、图像、音频、文件以及任何其他多模态内容。

from langchain.messages import SystemMessage,HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv  
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

model  = init_chat_model(
    model = "gpt-5.1",
    base_url = "http://localhost:8317/v1"
)

# Text content
response = model.invoke([
    HumanMessage("What is machine learning?")
])

# Message metadata
human_msg = HumanMessage(
    content = "Hello!",
    name = "alice",  # Optional: identify different users
    id = "msg_123"   # Optional: unique identifier for the message
)
# 名称字段的行为因提供者而异——有些用于用户识别，有些则忽略它。要检查，请参考模型提供者的参考。

