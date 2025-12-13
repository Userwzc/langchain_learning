# 在运行时选择相关工具以提升性能和准确性。
# 更简短的提示 - 仅暴露相关工具，以降低复杂性
# 更高的准确率 - 模型能从更少的选项中正确选择
# 权限控制 - 根据用户访问权限动态过滤工具


# Decorator 示例
from langchain.agents.middleware import wrap_model_call,ModelRequest,ModelResponse
from typing import Callable
from langchain.agents import create_agent

@wrap_model_call
def select_tools(
    request:ModelRequest,
    handler:Callable[[ModelRequest],ModelResponse]
) -> ModelResponse:
    """Middleware to select relevant tools based on the state/context."""
    # Select a small, relevant subset of tools based on state/context
    # relevant_tools = select_relevant_tools(request.state, request.runtime)
    # return handler(request.override(tools=relevant_tools))


# Class 示例
from langchain.agents.middleware import AgentMiddleware
class ToolSelectorMiddleware(AgentMiddleware):
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Middleware to select relevant tools based on state/context."""
        # Select a small, relevant subset of tools based on state/context
        # relevant_tools = select_relevant_tools(request.state, request.runtime)
        # return handler(request.override(tools=relevant_tools))

agent = create_agent(
    model="gpt-4o",
    tools="your_tools_here",  # All available tools need to be registered upfront
    middleware=[ToolSelectorMiddleware()],
)