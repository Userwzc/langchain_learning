# Matters:
# 当工具能够访问智能体状态、运行时上下文和长期记忆时，其能力最为强大。
# 这使得工具能够做出情境感知的决策、个性化响应，并在多次对话中保持信息连贯。
# 运行时上下文提供了一种在运行时将依赖项（如数据库连接、用户 ID 或配置）注入到工具中的方法，从而提高它们的可测试性和可重用性。

# 工具可以使用ToolRuntime参数访问运行时信息，该参数提供：
# - State: 在执行过程中流动的可变数据（例如消息、计数器、自定义字段）
# - Context： 不可变的配置信息，例如用户ID、会话详情或应用程序特定的配置
# - Store： 跨对话的持久化长期记忆
# - Strem Writer: 在工具执行时流式传输自定义更新
# - Config：执行时的RunnableConfig
# - Tool Call ID： 当前工具调用的ID

# 使用 ToolRuntime 可在单个参数中访问所有运行时信息。只需在工具签名中添加 runtime: ToolRuntime，它就会被自动注入，而不会暴露给 LLM。
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
load_dotenv()
os.getenv("OPENAI_API_KEY")

model = init_chat_model(
    model = "gpt-5.1",
    base_url = "http://localhost:8317/v1"
)
# Access the current conversation state
@tool
def summarize_conversation(runtime: ToolRuntime) -> str:
    """Summarize the conversation so far."""
    messages = runtime.state["messages"]

    human_msgs = sum(1 for m in messages if m.__class__.__name__ == "HumanMessage")
    ai_msgs = sum(1 for m in messages if m.__class__.__name__ == "AIMessage")
    tool_msgs = sum(1 for m in messages if m.__class__.__name__ == "ToolMessage")

    return f"Conversation has {human_msgs} user messages, {ai_msgs} AI responses, and {tool_msgs} tool results."

# Access custom config fields
@tool
def get_user_preference(pref_name: str, runtime: ToolRuntime) -> str:
    """Get a user preference value"""
    config = runtime.config.get("configurable", {})
    preferences = config.get("preferences", {})
    return preferences.get(pref_name, "Preference not set.")


human_msg = "用户的drink偏好是什么？"
agent = create_agent(
    tools = [get_user_preference],
    model = model,
    system_prompt="You are a helpful assistant that can access user preferences by using the get_user_preference tool."
)
response = agent.invoke({"messages": [("user", human_msg)]},
             config = {
                "configurable": {
                    "preferences": {
                        "language": "Chinese",
                        "drink": "coffee"
                    }
                }
             })

print(response)

# Updating state:
# Use `Command` to update the agent' state or control the graph's execution flow:
from langgraph.types import Command
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain.tools import tool, ToolRuntime

# Update the conversation history by removing all messages
@tool
def clear_conversation() -> Command:
    """Clear the conversation history."""
    # update 指示 LangGraph 更新状态
    return Command(
        update = {
            # "messages" 是状态中的键名（需与你的 State 定义一致）
            # RemoveMessage(id=REMOVE_ALL_MESSAGES) 是一个特殊操作，用于删除所有消息
            "message" : [RemoveMessage(id=REMOVE_ALL_MESSAGES)]
        }
    )

# Update the user_name in the agent state
@tool
def update_user_name(new_name: str, runtime: ToolRuntime) -> Command:
    """Update the user's name"""
    return Command(
        update = {
            # 直接将状态中的 "user_name" 字段更新为 new_name
            "user_name": new_name
        }
    )