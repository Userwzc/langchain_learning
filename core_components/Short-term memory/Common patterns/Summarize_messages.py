# 修剪或删除消息的问题在于，可能会因裁剪消息队列而丢失信息。
# 因此某些应用可以从一种更高级的方法中获益，即使用聊天模型对消息历史进行摘要

# 要在智能体中汇总历史消息，请使用内置的`SummarizationMiddleware`中间件

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317"
)

agent = create_agent(
    model = model,
    tools = [],
    middleware=[SummarizationMiddleware(model = model, trigger = ("tokens",4000),keep = ("messages", 20))],
    checkpointer=InMemorySaver()
)

config : RunnableConfig = {
    "configurable": {"thread_id": "1"}
}

agent.invoke({"messages": "hi, my name is bob"}, config)
agent.invoke({"messages": "write a short poem about cats"}, config)
agent.invoke({"messages": "now do the same but for dogs"}, config)
final_response = agent.invoke({"messages": "what's my name?"}, config)

print(final_response["messages"][-1].pretty_print())
