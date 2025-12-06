# ProviderStrategy 使用模型提供者的本地结构化输出生成。这更可靠，但仅适用于支持本地结构化输出的提供者（例如，OpenAI）：

from langchain.agents.structured_output import ProviderStrategy
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")


class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str


model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://127.0.0.1:8317/v1"
)

agent = create_agent(
    model = model,
    tools = [],
    response_format=ProviderStrategy(ContactInfo)
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]}
)

print(result["structured_response"])