from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime  # 用于定义工具和工具运行时
from dataclasses import dataclass  # 用于定义数据类
from langchain.chat_models import init_chat_model # 用于初始化聊天模型
from langgraph.checkpoint.memory import InMemorySaver # 用于内存保存
from langchain.agents.structured_output import ToolStrategy
from dotenv import load_dotenv
import os


load_dotenv()
os.getenv("DeepSeek_API_KEY")

@dataclass
class Context:
    """Custom runtime context schema."""
    user_id : str

# Define the system prompt
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""


# Create tools
@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's sunny in {city}."

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

# Configure the chat model
model = init_chat_model(
    model = "deepseek-chat",
    temperature = 0.5,
    timeout = 10,
    max_tokens = 1000
)

# define response format
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    punny_response: str
    weather_condition: str | None = None

# Add memory
# 为你的智能体添加记忆功能，以保持跨交互的状态。这使智能体能够记住之前的对话和上下文。

# Set up memory
checkpointer = InMemorySaver()

# Create and run the agent
agent = create_agent(
    model = model,
    system_prompt=SYSTEM_PROMPT,
    tools = [get_weather, get_user_location],
    response_format = ResponseFormat,
    context_schema=Context,
    checkpointer=checkpointer
)

# `thread_id` is a unique identifier for a given conversation.
config = {
    "configurable":{ 
        "thread_id" : "1"
    }
}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    config = config,
    context = Context(user_id = "1")
)

print(response['structured_response'])


response = agent.invoke(
    {"messages": [{"role": "user", "content": "thank you!"}]},
    config = config,
    context = Context(user_id="1")
)
print(response['structured_response'])
