# 当结构化输出与预期的模式不匹配时，代理会提供具体的错误反馈：
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv  
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

class ProductRating(BaseModel):
    rating: int | None = Field(description="Rating from 1-5", ge=1, le=5)
    comment: str = Field(description="Review comment")

model = ChatOpenAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317/v1"
)

agent = create_agent(
    model = model,
    response_format=ToolStrategy(
        schema=ProductRating),
    system_prompt="You are a helpful assistant that parses product reviews. Do not make any field or value up."
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Parse this: Amazing product, 10/10!"}]
})

for message in result["messages"]:
    message.pretty_print()