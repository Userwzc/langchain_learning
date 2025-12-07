# 一些模型提供商会将token使用信息作为调用响应的一部分返回。
# 当可用时，这些信息将被包含在相应模型生成的AIMessage对象中。

# 您可以使用回调或上下文管理器来跟踪应用程序中跨模型的聚合令牌计数.
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import UsageMetadataCallbackHandler
from langchain_core.callbacks import get_usage_metadata_callback
from dotenv import load_dotenv  
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

model_1 = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://localhost:8317/v1",
)

model_2 = ChatOpenAI(
    model = "gpt-5",
    base_url="http://localhost:8317/v1",
)

# callback = UsageMetadataCallbackHandler()

# result1 = model_1.invoke("hello",config = {"callbacks": [callback]})
# result2 = model_2.invoke("hello",config = {"callbacks": [callback]})
# print(callback.usage_metadata)

with get_usage_metadata_callback() as callback:
    model_1.invoke("hello")
    model_2.invoke("hello")
    print(callback.usage_metadata)

