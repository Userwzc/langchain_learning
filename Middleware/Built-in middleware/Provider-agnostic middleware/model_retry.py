# 自动使用可配置的指数退避策略重试失败的模型调用。
# 模型重试适用于以下场景:

# 处理模型 API 调用中的瞬时故障
# 提高依赖网络的模型请求的可靠性
# 构建能够优雅处理临时模型错误的弹性智能体

# API reference: ModelRetryMiddleware
# params:
# max_retries: number  default: "2"  初始调用后的最大重试次数（默认共尝试 3 次）

# retry_on: tuple[type[Exception],...] | callable default: "(Exception,)"
# 要么是一个包含要重试的异常类型的元组，
# 要么是一个可调用对象，该对象接收一个异常作为参数，并在应重试时返回 True

# on_failure: string | callable  default: "continue"
# 当所有重试次数用尽时的行为。选项：
# 'continue'（默认）——返回一个包含错误详情的 AIMessage，允许智能体有可能优雅地处理该失败情况
# 'error' - 重新抛出异常（停止智能体执行）
# 自定义可调用对象——一个接收异常并返回字符串的函数，用于 AIMessage 的内容

# backoff_factor: number  default: "2.0" 
# 指数退避的倍数。
# 每次重试等待 initial_delay * (backoff_factor ** retry_number) 秒。
# 设置为 0.0 表示使用固定延迟

# initial_delay: number   default: "1.0"  首次重试前的初始延迟时间（秒）

# max_delay: number  default: "60.0"   重试之间以秒为单位的最大延迟（限制指数退避增长）

# jitter: boolean  default： "true"   是否向延迟中添加随机抖动（±25%）以避免惊群效应

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware


# Basic usage with default settings (2 retries, exponential backoff)
agent = create_agent(
    model="gpt-4o",
    tools=["search_tool"],
    middleware=[ModelRetryMiddleware()],
)

# Custom exception filtering
class TimeoutError(Exception):
    """Custom exception for timeout errors."""
    pass

class ConnectionError(Exception):
    """Custom exception for connection errors."""
    pass

# Retry specific exceptions only
retry = ModelRetryMiddleware(
    max_retries=4,
    retry_on=(TimeoutError, ConnectionError),
    backoff_factor=1.5,
)


def should_retry(error: Exception) -> bool:
    # Only retry on rate limit errors
    if isinstance(error, TimeoutError):
        return True
    # Or check for specific HTTP status codes
    if hasattr(error, "status_code"):
        return error.status_code in (429, 503)
    return False

retry_with_filter = ModelRetryMiddleware(
    max_retries=3,
    retry_on=should_retry,
)

# Return error message instead of raising
retry_continue = ModelRetryMiddleware(
    max_retries=4,
    on_failure="continue",  # Return AIMessage with error instead of raising
)

# Custom error message formatting
def format_error(error: Exception) -> str:
    return f"Model call failed: {error}. Please try again later."

retry_with_formatter = ModelRetryMiddleware(
    max_retries=4,
    on_failure=format_error,
)

# Constant backoff (no exponential growth)
constant_backoff = ModelRetryMiddleware(
    max_retries=5,
    backoff_factor=0.0,  # No exponential growth
    initial_delay=2.0,  # Always wait 2 seconds
)

# Raise exception on failure
strict_retry = ModelRetryMiddleware(
    max_retries=2,
    on_failure="error",  # Re-raise exception instead of returning message
)