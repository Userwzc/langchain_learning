# 自动重试失败的工具调用，并支持配置指数退避策略。
# 工具重试适用于以下场景：
# 处理外部 API 调用中的瞬时故障
# 提高依赖网络的工具的可靠性
# 构建能够优雅处理临时错误的弹性智能体

# API reference: ToolRetryMiddleware
# params:
# max_retries: number default : "2" 初始调用后的最大重试次数（默认共尝试 3 次）

# tools: list[BaseTool | str ]  可选的工具列表或工具名称，用于应用重试逻辑。如果为 None，则应用于所有工具

# retry_on: tuple[type[Exception], ...] | callable  default: "(Exception,)"
# 要么是一个包含要重试的异常类型的元组，要么是一个可调用对象，该对象接收一个异常作为参数，并在应重试时返回 True

# on_failure: string | callable  default:"return_message"
# 当所有重试次数用尽时的行为。选项：
# 'continue' 返回一个包含错误详情的 ToolMessage（允许 LLM 处理失败情况）
# 'raise'  重新抛出异常（停止智能体执行）
# 自定义可调用对象——一个函数，接收异常作为参数，并返回一个字符串作为 ToolMessage 的内容

# backoff_factor: number  default: "2.0"
# 指数退避的倍数。
# 每次重试等待 initial_delay * (backoff_factor ** retry_number) 秒。\
# 设置为 0.0 表示使用固定延迟

# initial_delay: number  default: "1.0"   首次重试前的初始延迟时间（秒）

# max_delay: number  default: "60.0"   重试之间以秒为单位的最大延迟（限制指数退避增长）

# jitter: boolean  default: "true"   是否向延迟中添加随机抖动（±25%）以避免惊群效应

from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware

agent = create_agent(
    model = "gpt-4o",
    tools = ["search_tool", "database_tool","api_tool"],
    middleware=[
        ToolRetryMiddleware(
            max_retries = 3,
            backoff_factor= 2.0,
            initial_delay= 1.0,
            max_delay= 60.0,
            jitter = True,
            tools = ["api_tool"],
            retry_on = (ConnectionError, TimeoutError),
            on_failure= "continue"
        )
    ]
)