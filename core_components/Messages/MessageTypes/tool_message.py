# 对于支持工具调用的模型，AI消息可以包含工具调用。工具消息用于将单个工具执行的结果传回模型。
# 工具可以直接生成ToolMessage对象。下面，我们展示一个简单的例子。
from langchain.messages import ToolMessage,AIMessage,HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv  
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")


model  = init_chat_model(
    model = "gpt-5.1",
    base_url = "http://localhost:8317/v1"
)

ai_msg = AIMessage(
    content = [],
    tool_calls = [{
        "name": "get_weather",
        "args": {"location": "San Francisco"},
        "id": "call_123"
    }]
)

weather_result = "Sunny, 72°F"
tool_msg = ToolMessage(
    content = weather_result,
    tool_call_id = "call_123"
)
# Attributes:
# content: required string - 工具执行的结果。
# tool_call_id: required string - 关联的工具调用的唯一标识符。
# name: required string - 工具的名称（可选，如果工具调用中已经包含名称，则不需要)
# artifact: dict - 用于存储补充数据，这些数据不会发送给模型，但可以通过编程方式访问。这对于存储原始结果、调试信息或供下游处理的数据非常有用，同时不会使模型的上下文变得杂乱

messages = [
    HumanMessage("What's the weather like in San Francisco?"),
    ai_msg, # Model's tool call
    tool_msg # Tool execution result
]

response = model.invoke(messages)  # Model processes the result 
print(response)

