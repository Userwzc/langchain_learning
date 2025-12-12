# 通过在达到令牌限制时清除较旧的工具调用输出，同时保留最近的结果，来管理对话上下文。
# 这有助于在包含大量工具调用的长对话中保持上下文窗口的可控性。
# 上下文编辑适用于以下场景：

# 包含大量工具调用的长对话，超出令牌限制
# 通过移除不再相关的旧工具输出来降低 token 成本
# 仅在上下文中保留最近的 N 个工具结果

# API reference: ContextEditingMiddleware, ClearToolUsesEdit
# params:
# edits: list[ContextEdit]  default: "[ClearToolUsesEdit()]"
# 要应用的 ContextEdit 策略列表

# token_count_method: string  default: "approximate"
# Token 计数方法。选项：'approximate' 或 'model'

# ClearToolUsesEdit options:
# trigger: number  default: "100000"
# 触发编辑的令牌数量。当对话超过此令牌数量时，较旧的工具输出将被清除

# clear_at_least: number  default: "0"
# 编辑运行时需回收的最小令牌数量。若设为 0，则清除所需的所有内容

# keep: number  default: "3"
# 必须保留的最新工具结果的数量。这些结果永远不会被清除。

# clear_tool_inputs: boolean  default: "False"
# 是否清除 AI 消息中发起的工具调用参数。当设为 True 时，工具调用的参数将被替换为空对象

# exclude_tools: list[string]  default: "()"
# 要排除在清除操作之外的工具名称列表。这些工具的输出永远不会被清除。

# placeholder : string  default: "[cleared]"
# 已清除工具输出的占位文本。此内容替换了原始工具消息的内容。


from langchain.agents import create_agent
from langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit


agent = create_agent(
    model="gpt-4o",
    tools=["search_tool", "your_calculator_tool", "database_tool"],
    middleware=[
        ContextEditingMiddleware(
            edits=[
                ClearToolUsesEdit(
                    trigger=2000,
                    keep=3,
                    clear_tool_inputs=False,
                    exclude_tools=[],
                    placeholder="[cleared]",
                ),
            ],
        ),
    ],
)
