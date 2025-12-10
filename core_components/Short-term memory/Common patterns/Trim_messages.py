# 启用短期记忆后，长对话可能会超出LLM的上下文窗口。常见的解决方案包括：
# Trim messages: 移除前N条或后N条消息（在调用LLM之前）
# Delete messages： 从Langgraph状态中永久删除消息
# Summarize messages: 将历史中较早的消息进行总结，并用摘要替换它们
# Custom strategies: 自定义策略（例如，消息过滤等）

# 决定何时截断消息的一种方法是统计消息历史中的token数量，并在接近该限制时进行截断。
# 如果你使用的是Langchain,可以使用trim messages工具，指定要保留的token数量以及处理边界时所采用的`strategy`(例如，保留最后的`max_tokens`)
# 要修剪智能体中的消息历史记录，请使用@brefore_model中间件装饰器
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent,AgentState
from langchain.agents.middleware import before_model
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from typing import Any
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window."""
    messages = state["messages"]

    if len(messages) <= 3:
        return None # No changes needed
    
    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages

    return {
        "messages":[
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *new_messages
        ]
    }

model = ChatOpenAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317/v1"
)

# model = ChatGoogleGenerativeAI(
#     model = "gemini-2.5-flash",
#     base_url="http://localhost:8317"
# )


agent = create_agent(
    model = model,
    tools = [],
    middleware=[trim_messages],
    checkpointer=InMemorySaver()
)

config: RunnableConfig = {
    "configurable": {"thread_id": "1"}
}

agent.invoke({"messages": "hi, my name is bob"},config)
agent.invoke({"messages": "write a short poem about cats"},config)
agent.invoke({"messages": "now do the same but for dogs"}, config)
final_response = agent.invoke({"messages": "what's my name?"} ,config)

print(final_response["messages"][-1].pretty_print())