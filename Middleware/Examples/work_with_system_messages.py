# 在中间件中通过`ModelRequest`的`system_message`字段修改系统消息
# `system_message`字段包含一个`SystemMessage`对象（即使智能体是使用字符串形式的`system_prompt`初始化的）

# Example: Adding context to system message
from langchain.agents.middleware import warp_model_call, ModelRequest, ModelResponse
from langchain.messages import SystemMessage
from typing import Callable

@warp_model_call
def add_context(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    # Always work with content blocks
    new_content = list(request.system_message.content_blocks) + [
        {"type": "text", "text": "Additional context"}
    ]
    new_system_message = SystemMessage(content = new_content)
    return handler(request.override(system_message=new_system_message))

# Example: Working with cache control(Anthropic)
# 在使用 Anthropic 模型时，你可以使用带有缓存控制指令的结构化内容块来缓存大型系统提示：
@warp_model_call
def add_cached_context(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    # Always work with content blocks
    new_content = list(request.system_message.content_blocks) + [
        {
            "type": "text",
            "text": "Here is a large document to analyze:\n\n<document>...</document>",
            # content up until this point is cached
            "cache_control": {"type": "ephemeral"}
        }
    ]
    new_system_message = SystemMessage(content = new_content)
    return handler(request.override(system_message=new_system_message))

# Note:
# ModelRequest.system_message 始终是一个 SystemMessage 对象，即使该智能体是通过 system_prompt="string" 创建的
# 使用 SystemMessage.content_blocks 以块列表的形式访问内容，无论原始内容是字符串还是列表
# 修改系统消息时，请使用 content_blocks 并追加新的块，以保留现有结构
# 您可以直接将 SystemMessage 对象传递给 create_agent 的 system_prompt 参数，以实现缓存控制等高级用例