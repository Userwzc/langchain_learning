# LangChain 聊天模型可以通过 .profile 属性暴露一个支持的功能和能力的字典
# 模型配置数据允许应用程序动态地适应模型的能力。例如：
# 摘要中间件可以根据模型上下文窗口大小触发摘要。
# 在create_agent中的结构化输出策略可以自动推断（例如，通过检查对本地结构化输出功能的支持）。
# 模型输入可以根据支持的模态和最大输入令牌进行限制。

from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os   
load_dotenv()
os.getenv("OPENAI_API_KEY") 

# model = ChatOpenAI(
#     model = "gpt-5.1",
#     base_url="http://localhost:8317/v1"
# )

# Update the model's profile (Option 1 : quick fix)
custom_profile = {
    "max_input_tokens": 100_000,
    "tool_calling": True,
    "structured_output": True
}

model = init_chat_model("...",profile = custom_profile)

# 通过合并现有模型配置文件与额外的键值对来创建一个新的配置文件
new_profile = model.profile | {"key": "value"}
# 通过复制模型并设置新的配置文件来更新模型
model.model_copy(update={"profile": new_profile})

# Optiona 2： fix data upstream
# use the langchain-model-profiles CLI tool to pull the latest data from models.dev
# pip install langchain-model-profiles
# langchain-profiles refresh --provider <provider> --data-dir <data-dir>
