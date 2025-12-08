# System message : Tell the model how to behave and provide context for interactions.
# SystemMessage代表一组初始指令，用于引导模型的行为。
# 您可以使用系统消息来设定语气、定义模型的角色，并建立回答的指导方针。

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
# Basic instructions
system_msg = SystemMessage("You are a helpful coding assistant.")

message = [
    system_msg,
    HumanMessage("How do I create a REST API ?")
]

# Detailed persona
system_msg = SystemMessage("""
You are a senior Python developer with expertise in web frameworks.
Always provide code examples and explain your reasoning.
Be concise but thorough in your explanations.
""")
message = [
    system_msg,
    HumanMessage("How do I create a REST API ?")
]
response = model.invoke(message)