# 在某些应用中，你可能需要为特定模型禁用单个token的流式传输。这在以下情况下非常有用：
# 使用多智能体系统来控制哪些智能体流式输出其结果
# 混合使用支持流式传输的模型与不支持流式传输的模型
# 部署到LangSmith并希望阻止某些模型输出流式传输到客户端
# Set `streaming = False` 在初始化模型时

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os       
load_dotenv()
os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317",
    streaming = False  # 禁用流式传输
)

# 部署到 LangSmith 时，请对任何不希望将输出流式传输给客户端的模型设置 streaming=False。
# 此配置需在部署前于您的图代码中完成。

# 并非所有聊天模型集成都支持 streaming 参数。
# 如果你的模型不支持该参数，请改用 disable_streaming=True。此参数通过基类在所有聊天模型中均可使用。