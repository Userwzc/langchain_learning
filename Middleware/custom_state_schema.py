# 中间件可以通过自定义属性扩展代理的状态
# 这使得中间件能够：
# Track state across execution
# 跨执行过程跟踪状态 ：维护在整个智能体执行生命周期中持续存在的计数器、标志或其他值
# Share data between hooks
# 在钩子之间共享数据 ：将信息从 before_model 传递到 after_model，或在不同的中间件实例之间传递
# Implement cross-cutting concerns
# 实现横切关注点 ：在不修改核心智能体逻辑的情况下，添加诸如速率限制、使用情况跟踪、用户上下文或审计日志等功能
# Make conditional decisions
# 做出条件判断 ：利用累积的状态来决定是继续执行、跳转到不同的节点，还是动态修改行为

# Example
# Decorator
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.agents.middleware import AgentState, before_model, after_model
from typing_extensions import NotRequired
from typing import Any
from langgraph.runtime import Runtime

class CustomState(AgentState):
    model_call_count: NotRequired[int]
    user_id: NotRequired[str]

@before_model(state_schema=CustomState, can_jump_to=['end'])
def check_call_limit(state: CustomState, runtime: Runtime) -> dict[str, Any] | None:
    count = state.get("model_call_count", 0)
    if count > 10:
        return {"jump_to": "end"}
    return None

@after_model(state_schema=CustomState)
def increment_counter(state: CustomState, runtime: Runtime) -> dict[str, Any] | None:
    return {"model_call_count": state.get("model_call_count", 0) + 1}

agent = create_agent(
    model = "gpt-4o",
    middleware=[check_call_limit, increment_counter],
    tools = []
)

result = agent.invoke({
    "messages": [HumanMessage(content="Hello")],
    "model_call_count": 0,
    "user_id": "user-123"
})

# Class
from langchain.agents.middleware import AgentMiddleware

class CallCounterMiddleware(AgentMiddleware):
    state_schema = CustomState

    def before_model(self, state: CustomState, runtime: Runtime) -> dict[str, Any] | None:
        count = state.get("model_call_count", 0)
        if count > 10:
            return {"jump_to": "end"}
        return None

    def after_model(self, state: CustomState, runtime: Runtime) -> dict[str, Any] | None:
        return {"model_call_count": state.get("model_call_count", 0) + 1}
    
