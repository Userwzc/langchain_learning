# 你可以从图状态中删除消息，以管理消息历史
# 当你想要删除特定消息或清空整个消息历史时，这非常有用
# 要从图状态中删除消息，可以使用`RemoveMessage`
# 要使`RemoveMessage`生效，你需要使用带有`add_messagesreducer`的状态键
# 默认的`AgentState`提供了这一功能

# To remove specific messages:
# from langchain.messages import RemoveMessage

# def delete_messages(state):
#     messages = state["messages"]
#     if len(messages) > 2:
#         # remove the earliest two messages
#         return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}
    
# To remove all messages:
# from langgraph.graph.message import REMOVE_ALL_MESSAGES

# def delete_all_messages(state):
#     return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)]}

from langchain.messages import RemoveMessage
from langchain.agents import create_agent,AgentState
from langchain.agents.middleware import after_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("GOOGLE_API_KEY")

@after_model
def delete_messages(state: AgentState, runtime: Runtime) -> dict | None:
    """Remove old messages to keep conversation manageable."""
    messages = state["messages"]
    if len(messages) > 2:
        # remove the earliest two messages
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}
    return None

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317"
)

agent = create_agent(
    model = model,
    tools = [],
    system_prompt="Please be concise and to the point.",
    middleware=[delete_messages],
    checkpointer=InMemorySaver()
)

config : RunnableConfig = {
    "configurable": {"thread_id": "1"}
}

for event in agent.stream(
    {"messages": [{"role": "user", "content": "hi! I'm bob"}]},
    config=config,
    stream_mode="values"    
):
    print([(message.type, message.content) for message in event["messages"]])
    
for event in agent.stream(
    {"messages": [{"role": "user", "content": "what's my name?"}]},
    config = config,
    stream_mode="values"
):
    print([(message.type, message.content) for message in event["messages"]])