# 对于具有多个钩子或配置的复杂中间件而言更加强大。
# 当你需要为同一个钩子同时定义同步和异步实现，或者希望将多个钩子组合到单个中间件中时，请使用类

# Example
from langchain.agents.middleware import (
    AgentMiddleware,
    AgentState,
    ModelRequest,
    ModelResponse
)
from langchain.agents import create_agent
from langgraph.runtime import Runtime
from typing import Callable, Any

class LoggingMiddleware(AgentMiddleware):
    def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"About to call model with {len(state['messages'])} messages.")
        return None
    
    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        print(f"Model returned: {state['messages'][-1].content}")
        return None
    
agent = create_agent(
    model = "gpt-4o",
    middleware=[LoggingMiddleware()],
    tools = []
)