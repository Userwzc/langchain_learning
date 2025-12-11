# 对于不支持原生结构化输出的模型，LangChain 使用工具调用来实现相同的效果。
# 这适用于所有支持工具调用的模型，而大多数现代模型都具备这一能力。
# class ToolStrategy(Generic[SchemaT]):
#     schema: type[SchemaT]
#     tool_message_content: str | None
#     handle_errors: Union[
#         bool,
#         str,
#         type[Exception],
#         tuple[type[Exception], ...],
#         Callable[[Exception], str],
#     ]

# schema 支持：
# Pydantic models: BaseModel subclasses with field validation
# Dataclasses: Python dataclasses with type annotations
# TypedDict: Typed dictionary classes
# JSON Schema: Dictionary with JSON schema specification
# Union types: 联合类型 ：多种模式选项。模型将根据上下文选择最合适的模式。

# tool_message_content: 生成结构化输出时返回的工具消息的自定义内容，若未提供，则默认显示结构化响应数据的消息
# handle_errors: 结构化输出验证失败时的错误处理策略。默认为 True。
# True： 使用默认错误模板捕获所有错误
# str: 使用此自定义消息捕获所有错误
# type[Exception]：仅捕获此异常类型，并使用默认消息
# tuple[type[Exception], ...]：仅使用默认消息捕获这些异常类型
# Callable[[Exception], str]：返回错误信息的自定义函数
# False: 不重试，让异常向上抛出

from pydantic import BaseModel, Field
from typing import Literal,Union
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

class ProductReview(BaseModel):
    """Analysis of a product review."""
    rating: int | None = Field(description="The rating of the product", ge=1, le=5)
    sentiment: Literal["positive", "negative"] = Field(description="The sentiment of the review")
    key_points: list[str] = Field(description="The key points of the review. Lowercase, 1-3 words each.")

class CustomerComplaint(BaseModel):
    """A customer complaint about a product or service."""
    issue_type: Literal["product", "service", "shipping", "billing"] = Field(description="The type of issue")
    severity: Literal["low", "medium", "high"] = Field(description="The severity of the complaint")
    description: str = Field(description="Brief description of the complaint")

model = ChatOpenAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317/v1"
)

agent = create_agent(
    model = model,
    response_format=ToolStrategy(Union[ProductReview, CustomerComplaint])
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze this review: 'Great product: 5 out of 5 stars. Fast shipping, but expensive'"}]
})

print(result["structured_response"])
