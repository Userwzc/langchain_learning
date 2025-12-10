# 通过`ToolRuntime`在工具中访问短期记忆（状态）
# `ToolRuntime`参数对工具签名是隐藏的（因此模型看不到它)，但工具可以通过它访问状态

from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent, AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("GOOGLE_API_KEY")

class CustomState(AgentState):
    user_id : str

@tool
def get_user_info(runtime: ToolRuntime[CustomState]) -> str:
    """Look up user info"""
    user_id = runtime.state["user_id"]
    return "User is John Smith" if user_id == "user_123" else "Unknown user"

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317"
)

agent = create_agent(
    model = model,
    tools = [get_user_info],
    state_schema=CustomState
)

result = agent.invoke({
    "messages": "look up user information",
    "user_id": "user_123"
})

print(result["messages"][-1].content)

