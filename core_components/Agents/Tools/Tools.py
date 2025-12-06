from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location} is sunny."

# Configure the chat model
model = init_chat_model(
    model = "deepseek-chat",
    temperature = 0.5,
    timeout = 10,
    max_tokens = 1000
)

agent = create_agent(
    model = model,
    tools = [search, get_weather]
)