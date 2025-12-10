# 默认情况下，智能体使用AgentState来管理短期记忆，具体通过`messages`键来维护对话历史
# 你可以通过扩展AgentState以添加额外字段，自定义状态模式通过`state_schema`参数传递给`create_agent`
from langchain.agents import AgentState,create_agent
from langgraph.checkpoint.memory import InMemorySaver

class CustomAgentState(AgentState):
    user_id: str
    preference: dict

agent = create_agent(
    "gpt-5",
    tools = [],
    state_schema=CustomAgentState,
    checkpointer=InMemorySaver()
)

# Custom state can be passed in invoke
result = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Hello!"}],
        "user_id": "user_123",
        "preference": {"theme": "dark"}
    },
    {"configurable": {"thread_id": "1"}}
)
