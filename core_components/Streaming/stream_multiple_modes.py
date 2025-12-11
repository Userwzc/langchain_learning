# 你可以通过将流模式作为列表传递来指定多种流式传输模式
# 流式输出将是形如 (mode, chunk) 的元组，其中 mode 是流模式的名称，chunk 是该模式所流式传输的数据。

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

agent = create_agent(
    model = model,
    tools = [get_weather]
)

for stream_mode, chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    stream_mode=["updates", "custom"]
):
    print(f"stream mode: {stream_mode}")
    print(f"content: {chunk}")
    print("\n")