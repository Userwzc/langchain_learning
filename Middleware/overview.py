# 在每一步控制和自定义智能体的执行
# 中间件提供了一种更精细地控制代理内部行为的方式。中间件适用于以下场景：
# 通过日志记录、分析和调试来跟踪智能体行为
# 转换提示、工具选择和输出格式化
# 添加重试、备用方案和提前终止逻辑
# 应用速率限制、防护措施和PII检测

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware,HumanInTheLoopMiddleware
from langchain_google_genai import ChatGoogleGenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenAI(
    model="gemini-2.5-flash",
    base_url="http://localhost:8317"
)

# 通过将中间件传递给 create_agent 来添加中间件：
agent = create_agent(
    model = model,
    tools = [],
    middleware=[
        SummarizationMiddleware(),  # 自动总结长对话
        HumanInTheLoopMiddleware()]
)

# The agent loop
# 核心智能体循环包括调用模型，让其选择要执行的工具，并在不再调用任何工具时结束
# 中间件在上述每个步骤之前和之后都提供了钩子