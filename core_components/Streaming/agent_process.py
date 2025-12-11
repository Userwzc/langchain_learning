# 要流式传输代理进度，请使用 stream 或 astream 方法，并设置 stream_mode="updates"。
# 这将在每次代理步骤后发出一个事件。
# 例如：如果你有一个代理调用了一次工具，你应该会看到以下更新：
# LLM node: AIMessage with tool call requests
# Tool node: ToolMessage with execution result
# LLM node: Final AI response

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
    model=model,
    tools=[get_weather],
)

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    stream_mode="updates"
):
    for step,data in chunk.items():
        print(f"step: {step}")
        # print(f"content: {data['messages'][-1].content_blocks}")
        print(f"content: {data['messages'][-1].pretty_print()}")
    # print(chunk)