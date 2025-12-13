# Wrap-style hooks  包装式钩子
# 拦截执行并控制handler调用的时机。可用于重试、缓存和转换
# 你可以决定handler是调用零次（短路）、一次（正常流程），还是多次（重试逻辑）
# Available hooks:
# wrap_model_call  around each model call
# wrap_tool_call  around each tool call

# Example
# Decorator
from langchain.agents.middleware import wrap_model_call,wrap_tool_call,ModelResponse,ModelRequest
from typing import Callable

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

# Class
from langchain.agents.middleware import AgentMiddleware

class RetryMiddleware(AgentMiddleware):
    def __init__(self, max_retries: int = 3):
        super().__init__()
        self.max_retries = max_retries
    
    def wrap_model_call(self, request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
        for attempt in range(self.max_retries):
            try:
                return handler(request)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                print(f"Retry {attempt + 1} / {self.max_retries} after error:{e}")

# When to use classes:
# 为同一个钩子同时定义同步和异步实现
# 单个中间件中需要多个钩子
# 需要复杂配置（例如，可配置的阈值、自定义模型）
# 通过初始化时的配置在多个项目中复用