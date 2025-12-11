# 要流式传输LLM生成的token,请使用`stream_mode="messages"`
# 下面你可以看到代理流式传输工具调用和最终响应的输出

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317"
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}"

agent = create_agent(
    model = model,
    tools = [get_weather],
)

for token,metadata in agent.stream(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    stream_mode="messages"
):
    print(f"node: {metadata['langgraph_node']}")
    print(f"content: {token.content_blocks}")
    print("\n")