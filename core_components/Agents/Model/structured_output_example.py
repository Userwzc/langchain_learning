from langchain_deepseek import ChatDeepSeek
from langchain.tools import tool
from pydantic import BaseModel, Field
# 假设 create_agent 是用户环境中可用的 API，类似于 langgraph 的 create_react_agent
from langchain.agents import create_agent 

# 1. 定义工具
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# 2. 定义结构化输出 Schema
class MathResponse(BaseModel):
    result: int = Field(description="The result of the calculation")
    explanation: str = Field(description="Explanation of the step")

# 3. 初始化模型
model = ChatDeepSeek(model="deepseek-chat")

# ==========================================
# 错误示范：使用预绑定模型 (Pre-bound model)
# ==========================================
print("--- 错误示范 ---")
# 这里的 model_with_tools 已经显式绑定了工具
model_with_tools = model.bind_tools([add])

try:
    # 当指定 response_format 时，Agent 内部需要完全控制模型的工具绑定状态
    # 以便注入结构化输出的 Schema。
    # 如果传入已经绑定了工具的模型，会发生冲突或报错。
    agent_error = create_agent(
        model=model_with_tools,  # <--- 错误：传入了预绑定模型
        tools=[add],
        response_format=MathResponse 
    )
    print("Agent created (Unexpected)")
except Exception as e:
    print(f"创建 Agent 失败 (预期内): {e}")
    print("原因：在使用 response_format 时，create_agent 需要原始模型来配置结构化输出，不能接受已经 bind_tools 的模型。")

# ==========================================
# 正确示范：使用原始模型 (Raw model)
# ==========================================
print("\n--- 正确示范 ---")
agent_success = create_agent(
    model=model,  # <--- 正确：传入原始模型
    tools=[add],
    response_format=MathResponse
)
print("Agent 创建成功。create_agent 会自动处理工具绑定和结构化输出配置。")
