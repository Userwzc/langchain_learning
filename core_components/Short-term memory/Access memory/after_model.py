# 在`@after_model`中间件中访问短期记忆（状态），以在模型调用后处理消息

from langchain.messages import RemoveMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent,AgentState
from langchain.agents.middleware import after_model
from langgraph.runtime import Runtime
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317"
)

@after_model
def validate_response(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove messages containing sensitive words."""
    STOP_WORDS = ["password", "secret"]
    last_message = state["messages"][-1]
    if any(word in last_message.content for word in STOP_WORDS):
        return {"messages": [RemoveMessage(id = last_message.id)]}
    return None

agent = create_agent(
    model = model,
    tools = [],
    middleware=[validate_response],
    checkpointer=InMemorySaver()
)