# 要自定义工具错误处理方式，请使用 @wrap_tool_call 装饰器来创建中间件：
from langchain.agents.middleware import wrap_tool_call
from langchain.agents import create_agent
from langchain.messages import ToolMessage
from Tools import search, get_weather

@wrap_tool_call
def handle_tool_errors(request, handler):
    """handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        # return a custom error message to the model
        return ToolMessage(
            content = f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id = request.tool_call["id"]
        )
    
agent = create_agent(
    model = "gpt-4o",
    tools = [search, get_weather],
    middleware=[handle_tool_errors]
)

