# 使用 state_schema 参数作为快捷方式来定义仅在工具中使用的自定义状态。


# 自 langchain 1.0 版本起，自定义状态模式必须为 TypedDict 类型。
# Pydantic 模型和数据类不再受支持。

# 通过中间件定义自定义状态比在 create_agent 中通过 state_schema 定义更受推荐，
# 因为它允许您将状态扩展在概念上限定在相关的中间件和工具范围内。
# state_schema 在 create_agent 中仍然支持以保持向后兼容性。
from langchain.agents import AgentState, create_agent
from langchain_openai import ChatOpenAI

class CustomState(AgentState):
    user_perferences: dict

model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://127.0.0.1:8317/v1"
)

agent = create_agent(
    model = model,
    tools = [],
    state_schema=CustomState
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "I perfer technical explanations."}],
     "user_perferences": {"style": "technical", "verbosity": "detailed"}}
)