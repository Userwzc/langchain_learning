# 一些模型提供商通过其 API 原生支持结构化输出（例如 OpenAI、Grok、Gemini）。在可用的情况下，这是最可靠的方法。
# 要使用此策略，请配置一个 ProviderStrategy：
# class ProviderStrategy(Generic[SchemaT]):
#     schema: type[SchemaT]

# schema 支持：
# Pydantic models: BaseModel subclasses with field validation
# Dataclasses: Python dataclasses with type annotations
# TypedDict: Typed dictionary classes
# JSON Schema: Dictionary with JSON schema specification

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

class ContactInfo(BaseModel):
    name: str = Field(description = "Full name of the person")
    email: str = Field(description = "The email address of the person")
    phone: str = Field(description = "The phone number of the person")

model = ChatOpenAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317/v1"
)

agent = create_agent(
    model = model,
    response_format=ContactInfo,
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

print(result["structured_response"])
