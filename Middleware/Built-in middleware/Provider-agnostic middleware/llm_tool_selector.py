# 使用 LLM 在调用主模型之前智能地选择相关工具。
# LLM 工具选择器适用于以下场景：
# 拥有大量工具（10个以上）的智能体，其中大多数工具在每次查询中并不相关
# 通过过滤无关工具来减少令牌使用量
# 提升模型的专注度与准确性

# 该中间件使用结构化输出，向 LLM 询问哪些工具与当前查询最相关。
# 结构化输出的模式定义了可用工具的名称和描述。模型提供商通常会在后台将此结构化输出信息添加到系统提示中。

# API reference: LLMToolSelectorMiddleware
# params:
# model: string | BaseChatModel  用于工具选择的模型，默认使用代理的主模型
# system_prompt: string  选择模型的指令。若未指定，则使用内置提示
# max_tools: number  最多选择的工具数量。如果模型选择的数量超过此值，则仅使用前 max_tools 个工具。若未指定，则无限制。
# always_include: list[string]   无论选择如何都始终包含的工具名称。这些工具不计入 max_tools 限制

from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolSelectorMiddleware

# agent = create_agent(
#     model="gpt-4o",
#     tools=[tool1, tool2, tool3, tool4, tool5, ...],
#     middleware=[
#         LLMToolSelectorMiddleware(
#             model="gpt-4o-mini",
#             max_tools=3,
#             always_include=["search"],
#         ),
#     ],
# )