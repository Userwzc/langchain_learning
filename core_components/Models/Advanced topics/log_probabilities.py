# 某些模型可以通过在初始化模型时设置logprobs参数来配置，
# 以返回表示给定标记可能性的标记级对数概率

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("DEEPSEEK_API_KEY")

model = init_chat_model(
    "deepseek-chat"
).bind(logprobs=True)

response = model.invoke("Why do parrots talk?")
print(response.response_metadata["logprobs"])