from langchain.messages import SystemMessage, HumanMessage,AIMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv  
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

model  = init_chat_model(
    model = "gpt-5.1",
    base_url = "http://localhost:8317/v1"
)

# 在以下情况使用消息提示
# - 管理多轮对话
# - 处理多模态内容
# - 包含系统指令

message = [
    SystemMessage("You are a helpful assistant."),
    HumanMessage("Hello, how are you?"),
    AIMessage("I'm fine, thank you! How can I assist you today?")
]

response = model.invoke(message)  