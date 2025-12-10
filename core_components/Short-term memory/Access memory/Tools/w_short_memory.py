# 在工具执行过程中，若要修改智能体的短期记忆（状态）,可以直接从工具中返回状态更新
# 这有助于持久化中间结果，或使信息可供后续工具或提示使用

from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent, AgentState
from langchain_core.runnables import RunnableConfig
from langchain.messages import ToolMessage
from langgraph.types import Command
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317"
)

class CustomState(AgentState):
    user_name: str

class CustomContext(BaseModel):
    user_id: str

@tool
def update_user_info(runtime: ToolRuntime[CustomContext,CustomState]) -> Command:
    """Look up and update user info"""
    user_id = runtime.context.user_id
    name  = "John Smith" if user_id == "user_123" else "Unknown User"
    return Command(update={
        "user_name": name,
        "messages": [
            ToolMessage("Successfully updated user information.Please call the `greet` tool to greet the user.",
                        tool_call_id = runtime.tool_call_id)
        ]
    })

@tool
def greet(runtime: ToolRuntime[CustomContext,CustomState]) -> str | Command:
    """Use this to greet the user once you found their info."""
    user_name = runtime.state.get("user_name", None)
    if user_name is None:
        return Command(update={
            "messages": [
                ToolMessage("Please call the `update_user_info` tool it will get and update the user's name.",
                            tool_call_id = runtime.tool_call_id)
            ]
        })
    return f"Hello, {user_name}!"

agent = create_agent(
    model = model,
    tools = [update_user_info, greet],
    state_schema=CustomState,
    context_schema=CustomContext,
    system_prompt="You are a helpful assistant that greets users by their names.if you don't know the user's name, use the `greet` tool to greet them."
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "greet the user"}]},
    context=CustomContext(user_id="user_123")
)

for message in response["messages"]:
    print(message.pretty_print())