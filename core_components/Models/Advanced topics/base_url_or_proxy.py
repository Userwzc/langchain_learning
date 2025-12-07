# 对于许多聊天模型的集成，您可以配置 API 请求的基本 URL，
# 这允许您使用具有 OpenAI 兼容 API 的模型提供者或使用代理服务器。

from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

model = init_chat_model(
    model = "Model-Name",
    model_provider="provider-name",
    base_url="BASE_URL",  # 替换为您的模型提供者的基本 URL
    # api_key="your-api-key"  # 如果需要，提供 API 密钥
)

model = ChatOpenAI(
    model = "gpt-5.1",
    openai_proxy ="http://proxy.example.com:8080"
)
