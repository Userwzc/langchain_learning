# Models can be utilized in two ways:
# 1. With agents
# 2.Standalone

from langchain_deepseek import ChatDeepSeek
from langchain.chat_models import init_chat_model

# 1. Using Model Class
model = ChatDeepSeek(
    model="deepseek-chat"
)

# 2. Using init_chat_model utility
model = init_chat_model(
    "deepseek-chat"
)

# Parameters(标准参数)
# model （required)
# api_key
# temperature
# max_tokens  Limits the total number of tokens in the response, effectively controlling how long the output can be.
# timeout  在取消请求之前，等待模型响应的最大时间（以秒为单位）。
# max_retries   系统在因网络超时或速率限制等问题导致请求失败时，将尝试重新发送请求的最大次数。