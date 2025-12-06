# 智能体通过消息状态自动维护对话历史。您还可以配置智能体使用自定义状态模式，以便在对话过程中记住更多信息。
# 存储在状态中的信息可以被视为智能体的短期记忆：
# 自定义状态模式必须扩展 AgentState 作为 TypedDict。
# 定义自定义状态有两种方法：
# 通过中间件（推荐）
# 通过 create_agent 上的 state_schema

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_openai import ChatOpenAI
from typing import Any

# 当您的自定义状态需要被附加到特定中间件挂钩和工具访问时，使用中间件来定义自定义状态。
# 这种方式允许您将状态管理逻辑封装在中间件中，使主 Agent 逻辑更清晰。

class CustomState(AgentState):
    """自定义状态模式，扩展了基础的 AgentState。
    除了默认的 messages 外，还包含用户偏好信息。
    """
    user_perferences : dict

class CustomMiddleware(AgentMiddleware):
    """自定义中间件，用于处理用户偏好。
    通过定义 state_schema，告知 Agent 需要管理 CustomState 中定义的额外字段。
    """
    state_schema = CustomState
    tools = []
    
    def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
        """在模型调用之前执行的钩子。
        可以在这里根据 state['user_perferences'] 修改提示词或模型参数。
        """
        # 示例逻辑：实际应用中可以在这里读取偏好并调整行为
        # print(f"当前用户偏好: {state.get('user_perferences')}")
        ...

model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://127.0.0.1:8317/v1"
)

agent = create_agent(
    model = model,
    tools = [],
    middleware=[CustomMiddleware()]
)

# The agent can now track additonal state beyond messages
# 在调用 invoke 时，可以直接传入自定义状态字段（如 user_perferences）。
# 这些数据会被注入到 Agent 的状态中，并流经中间件。
result = agent.invoke(
    {"messages": [{"role": "user", "content": "I perfer technical explanations."}],
     "user_perferences": {"style": "technical", "verbosity": "detailed"}}
)