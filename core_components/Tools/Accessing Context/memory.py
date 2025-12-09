# 通过store在对话之间访问持久化数据。
# store可通过`runtime.store`访问,允许你保存和检索用户特定或应用特定的数据

from typing import Any
from langgraph.store.memory import InMemoryStore
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

# Access memory
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up user info"""
    store = runtime.store
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "User not found."

# Update memory
@tool
def save_user_info(user_id: str, user_info: dict[str, Any], runtime: ToolRuntime) -> str:
    """Save user info"""
    store = runtime.store
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info."

store = InMemoryStore()

agent = create_agent(
    tools = [get_user_info, save_user_info],
    model = ChatOpenAI(model="gpt-5.1", base_url="http://localhost:8317/v1"),
    store = store
)

# First session: save user info
agent.invoke({
    "messages": [{"role": "user", "content": "Save the following user: userid: abc123, name: Foo, age: 25, email: foo@langchain.dev"}]
})

# Second session: get user info
result = agent.invoke({
    "messages": [{"role": "user", "content": "Get the info for user with userid: abc123"}]
})

print(result["messages"][-1].content)  # Should print the user info saved earlier
