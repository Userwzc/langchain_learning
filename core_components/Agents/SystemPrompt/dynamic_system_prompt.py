# 在更高级的使用场景中，如果您需要根据运行时上下文或代理状态来修改系统提示，您可以使用中间件。
# @dynamic_prompt 装饰器创建基于模型请求生成系统提示的中介件：
from typing import TypedDict
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

class Context(TypedDict):
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user role in context."""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "You are an AI assistant."

    if user_role == "expert":
        return f"{base_prompt} Provide detailed and technical responses."
    elif user_role == "beginner":
        return f"{base_prompt} Explain concepts in simple terms suitable for beginners."
    
    return base_prompt

agent = create_agent(
    model = "deepseek-chat",
    tools = [],
    middleware=[user_role_prompt],
    context_schema=Context
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Explain quantum computing."}]},
    context = {"user_role": "expert"}
)
