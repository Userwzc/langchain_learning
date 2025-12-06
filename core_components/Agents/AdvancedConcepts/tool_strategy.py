# ToolStrategy 使用人工工具调用来生成结构化输出。这适用于任何支持工具调用的模型：
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from dotenv import load_dotenv
import os


load_dotenv()
os.getenv("DeepSeek_API_KEY")

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

agent = create_agent(
    model = "deepseek-chat",
    tools = [],
    response_format=ToolStrategy(ContactInfo)
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]}
)

print(result["structured_response"])