# 要从工具执行过程中流式获取更新，可以使用`get_stream_writer`

from langchain.agents import create_agent
from langgraph.config import get_stream_writer
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
    writer = get_stream_writer()
    # stream any arbitrary data
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}"

# ？如果你在工具内部添加了`get_stream_writer`，你将无法在LangGraph执行上下文之外调用该工具

agent = create_agent(
    model = model,
    tools = [get_weather],
)

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    stream_mode="custom"
):
    print(f"custom data: {chunk}")