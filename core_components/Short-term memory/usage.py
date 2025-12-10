# 短期记忆使你的应用程序能够在单个线程或对话中记住之前的交互
# 一个线程将一次会话的多次交互组织在一起，类似于电子邮件将消息归入同一对话的方式

# 要为智能体添加短期记忆（线程级持久化），在创建智能体时需要指定一个`checkpointer`
# Langchain的智能体将短期记忆作为其状态的一部分进行管理
# 通过将这些内容存储在图的状态中，智能体可以在保持不同对话线程相互隔离的同时，访问特定对话的完整上下文
# 状态通过检查点(checkpointer)持久化到数据库（或内存）中，以便随时恢复该线程
# 短期记忆在代理被调用或一个步骤（如工具调用）完成时更新，并在每个步骤开始时读取状态
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool, ToolRuntime

# Access memory
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up user info"""
    store = runtime.store
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "User not found."


agent = create_agent(
    "gpt-5",
    tools = [get_user_info],
    checkpointer=InMemorySaver()
)

agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    {"configurable": {"thread_id": "1"}}
)

# In production
# pip install langgraph-checkpoint-postgres
from langgraph.checkpoint.postgres import PostgresSaver

DB_URL = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    checkpointer.setup() # auto create tables in PostgresSql
    agent = create_agent(
        "gpt-5",
        tools = [get_user_info],
        checkpointer=checkpointer
    )
