# LLM 工具模拟器
# 使用 LLM 模拟工具执行以进行测试，用 AI 生成的响应替代实际的工具调用。
# LLM 工具模拟器适用于以下场景：

# 在不执行真实工具的情况下测试智能体行为
# 在外部工具不可用或成本高昂时开发智能体
# 在实现实际工具之前，对智能体工作流进行原型设计


# API reference: LLMToolEmulator
# params:
# tools : list[str | BaseTool ] 
# 要模拟的工具名称（str）或 BaseTool 实例的列表。
# 如果为 None（默认值），将模拟所有工具；如果为空列表 []，则不模拟任何工具；
# 如果为包含工具名称或实例的数组，则仅模拟这些指定的工具

# model : string | BaseChatModel
# 用于生成模拟工具响应的模型,若未指定，则默认使用智能体的模型

# 该中间件使用 LLM 为工具调用生成合理的响应，而不是执行实际的工具

from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolEmulator
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"Weather in {location}"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    return "Email sent"

# Emulate all tools (default behavior)
agent = create_agent(
    model = "gpt-4o",
    tools = [get_weather, send_email],
    middleware=[
        LLMToolEmulator()
    ]
)

# Emulate specific tools only
agent2 = create_agent(
    model = "gpt-4o",
    tools = [get_weather, send_email],
    middleware=[
        LLMToolEmulator(tools=["get_weather"])
    ]
)

# Use custom model for emulation
agent3 = create_agent(
    model = "gpt-4o",
    tools = [get_weather, send_email],
    middleware=[
        LLMToolEmulator(
            model="gpt-4o-mini"
        )
    ]
)