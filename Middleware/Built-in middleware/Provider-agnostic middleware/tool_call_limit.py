# 通过限制工具调用次数来控制代理的执行，既可以对所有工具全局限制，也可以针对特定工具进行限制。
# 工具调用限制适用于以下场景：
# 防止对外部昂贵 API 的过度调用。
# 限制网络搜索或数据库查询。
# 对特定工具的使用实施速率限制。
# 防止代理陷入无限循环。

# API reference: ToolCallLimitMiddleware
# params:
# tool_name: string   要限制的特定工具名称。如果未提供，则限制将应用于所有工具（全局）。
# thread_limit: number  
# 一个线程（对话）中所有运行期间的最大工具调用次数。
# 在使用相同线程 ID 的多次调用中保持不变。
# 需要一个检查点器（checkpointer）来维持状态。
# None 表示不对线程设置限制。
# run_limit: number
# 单次调用（一次用户消息 → 响应周期）中工具调用的最大次数。每次新的用户消息都会重置该限制。None 表示无运行次数限制。
# exit_behavior: string  default: 'continue'
# 达到限制时的行为：
# 'continue'（默认）——当工具调用超出限制时，以错误消息阻断该工具，但允许其他工具和模型继续运行。模型会根据错误消息自行决定何时结束
# 'error' - 抛出一个 ToolCallLimitExceededError 异常，立即停止执行
# 'end' - 立即停止执行，并为超出限制的工具调用返回一个 ToolMessage 和 AI 消息。仅在限制单个工具时有效；如果其他工具存在待处理的调用，则会抛出 NotImplementedError


from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware

agent = create_agent(
    model="gpt-4o",
    tools=["search_tool", "database_query_tool"],
    middleware=[
        # Global limit
        ToolCallLimitMiddleware(thread_limit = 20, run_limit = 10),
        # Tool-specific limit
        ToolCallLimitMiddleware(
            tool_name = "search",
            thread_limit = 5,
            run_limit = 3
        )
    ]
)

# global_limiter = ToolCallLimitMiddleware(thread_limit=20, run_limit=10)
# search_limiter = ToolCallLimitMiddleware(tool_name="search", thread_limit=5, run_limit=3)
# database_limiter = ToolCallLimitMiddleware(tool_name="query_database", thread_limit=10)
# strict_limiter = ToolCallLimitMiddleware(tool_name="scrape_webpage", run_limit=2, exit_behavior="error")

# agent = create_agent(
#     model="gpt-4o",
#     tools=[search_tool, database_tool, scraper_tool],
#     middleware=[global_limiter, search_limiter, database_limiter, strict_limiter],
# )


