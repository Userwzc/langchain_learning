# 模型在通过工具调用生成结构化输出时可能会出错。LangChain 提供了智能重试机制，可自动处理这些错误。

# 当模型错误地调用了多个结构化输出工具时，智能体会在 ToolMessage 中提供错误反馈，并提示模型重试：
from pydantic import BaseModel, Field
from typing import Union
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

class ContactInfo(BaseModel):
    name: str = Field(description="Person's name")
    email: str = Field(description="Email address")

class EventDetails(BaseModel):
    event_name: str = Field(description="Name of the event")
    date: str = Field(description="Event date")

model = ChatOpenAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317/v1"
)

agent = create_agent(
    model= model,
    tools=[],
    response_format=ToolStrategy(Union[ContactInfo, EventDetails])  # Default: handle_errors=True
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]
})

for message in result["messages"]:
    message.pretty_print()