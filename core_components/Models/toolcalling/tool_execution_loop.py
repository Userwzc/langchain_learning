from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://localhost:8317/v1"
)

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

model_with_tool = model.bind_tools([get_weather])
# 使用tool_choice来使模型使用任何工具或特定的工具
# model_with_tools = model.bind_tools([tool_1], tool_choice="tool_1")
# model_with_tools = model.bind_tools([tool_1], tool_choice="any")
# 大多数支持工具调用的模型默认启用并行工具调用。部分模型（包括 OpenAI 和 Anthropic）允许你禁用此功能。
# 要禁用该功能，请设置 parallel_tool_calls=False
# model.bind_tools([get_weather], parallel_tool_calls=False)

# 在绑定用户自定义工具时，模型的响应会包含一个执行工具的请求。
# 当单独使用模型而不使用代理时，您需要执行请求的工具并将结果返回给模型，以便在后续推理中使用。
# 当使用代理时，代理循环将为您处理工具执行循环。


print("\n--- Tool Execution Loop Example ---\n")

# Step 1: Model generates tool calls
messages = [
    {"role": "user", "content": "What's the weather like in New York?"}
]

ai_msg = model_with_tool.invoke(messages)
# print(ai_msg)
messages.append(ai_msg)

# Step 2: Execute tools and collect results
for tool_call in ai_msg.tool_calls:
    # Execute the tool with the generated arguments
    tool_result = get_weather.invoke(tool_call)
    # 每个工具返回的ToolMessage都包含一个与原始工具调用匹配的工具调用ID，这有助于模型将结果与请求相关联。
    messages.append(tool_result)

# Step 3: Pass results back to the model for final response
final_response = model_with_tool.invoke(messages)
print(final_response.text)


# Parallel Tool Execution Loop Example
print("\n --- Parallel Tool Execution Loop Example ---\n")

response = model_with_tool.invoke(
    "What's the weather like in New York and San Francisco?"
)

# The model may generate multiple tool calls
print(response.tool_calls)

# Execute all tools (can be done in parallel with async code)
results = []
for tool_call in response.tool_calls:
    if tool_call["name"] == "get_weather":
        result = get_weather.invoke(tool_call)

    results.append(result)
print(results)