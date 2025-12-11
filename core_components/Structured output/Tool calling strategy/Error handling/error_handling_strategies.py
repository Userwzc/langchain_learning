# 你可以使用 handle_errors 参数来自定义错误的处理方式：


## Custom error message:
# ToolStrategy(
#     schema=ProductRating,
#     handle_errors="Please provide a valid rating between 1-5 and include a comment."
# )

# 如果 handle_errors 是一个字符串，代理将始终提示模型使用固定的工具消息重试：
# ================================= Tool Message =================================
# Name: ProductRating

# Please provide a valid rating between 1-5 and include a comment.

## Handle specific exceptions only:
# ToolStrategy(
#     schema=ProductRating,
#     handle_errors=ValueError  # Only retry on ValueError, raise others
# )

# 如果 handle_errors 是一种异常类型，则仅当抛出的异常属于指定类型时，
# 代理才会重试（使用默认错误消息）；在所有其他情况下，异常将被直接抛出。


## Handle multiple exception types:
# ToolStrategy(
#     schema=ProductRating,
#     handle_errors=(ValueError, TypeError)  # Retry on ValueError and TypeError
# )

# 如果 handle_errors 是一个异常元组，则仅当抛出的异常属于指定类型之一时，
# 代理才会重试（使用默认错误消息）；在所有其他情况下，异常将被直接抛出。


## Custom error handler function:
from langchain.agents.structured_output import StructuredOutputValidationError
from langchain.agents.structured_output import MultipleStructuredOutputsError
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from typing import Union
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

def custom_error_handler(error: Exception) -> str:
    if isinstance(error, StructuredOutputValidationError):
        return "There was an issue with the format. Try again."
    elif isinstance(error, MultipleStructuredOutputsError):
        return "Multiple structured outputs were returned. just pick one."
    else:
        return f"Error: {str(error)}"
    
model = ChatOpenAI(
    model = "kimi-k2",
    base_url="http://localhost:8317/v1"
)

agent = create_agent(
    model = model,
    tools = [],
    response_format=ToolStrategy(
        schema = Union[ContactInfo, EventDetails],
        # handle_errors=custom_error_handler
    )
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract info: John Doe (john@email.com) is organizing Tech Conference on March 15th"}]
})
# print(result)

# for msg in result["messages"]:
#     msg.pretty_print()

for msg in result["messages"]:
    # If message is actually a ToolMessage object (not a dict), check its class name
    if type(msg).__name__ == "ToolMessage":
        print(msg.content)
    # If message is a dictionary or you want a fallback
    elif isinstance(msg, dict) and msg.get("tool_call_id"):
        print(msg['content'])
    