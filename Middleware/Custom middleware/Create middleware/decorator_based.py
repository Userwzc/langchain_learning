# 你可以创建中间件通过两种方式
# 1.Decorator-based
# 适用于单钩子中间件的快速简便方法，使用装饰器来包装单个函数
# 2.Class-based
# 对于具有多个钩子或配置的复杂中间件来说更加强大

# Example
from langchain.agents.middleware import before_model,wrap_model_call,AgentState,ModelRequest,ModelResponse
from langchain.agents import create_agent
from langgraph.runtime import Runtime
from typing import Callable, Any

@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"About to call model with {len(state['messages'])} messages.")
    return None

@wrap_model_call
def retry_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    for attempt in range(3):
        try:
            return handler(request)
        except Exception as e:
            if attempt == 2:
                raise
            print(f"Retry {attempt + 1} / 3 after error:{e}")

agent = create_agent(
    model = "gpt-4o",
    middleware=[log_before_model, retry_model],
    tools = []
)

# When to use decorators:
# Single hook needed
# No complex configuration
# Quick prototyping