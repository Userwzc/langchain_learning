from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://localhost:8317/v1"
)

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

model_with_tool = model.bind_tools([get_weather])

response = model_with_tool.invoke(
    "What's the weather like in New York?"
)

for tool_call in response.tool_calls:
    # View tool call made by the model
    print(f"Tool : {tool_call['name']}")
    print(f"Args : {tool_call['args']}")

