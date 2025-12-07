# 许多聊天模型提供商会对在给定时间段内可以调用的次数设置限制。如果你达到了速率限制，
# 你通常会从提供者那里收到一个速率限制错误响应，并且需要等待才能进行更多请求。

# 为了帮助管理速率限制，
# 聊天模型集成接受一个rate_limiter参数，该参数可以在初始化时提供，以控制请求的速率。

from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_openai import ChatOpenAI
rate_limiter = InMemoryRateLimiter(
    request_per_second = 0.1, # 10秒1次请求
    check_every_n_seconds= 0.1, # 每100毫秒检查是否允许发起请求
    max_bucket_size=10, # 控制最大突发大小
)

model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://localhost:8317/v1",
    rate_limiter=rate_limiter
)