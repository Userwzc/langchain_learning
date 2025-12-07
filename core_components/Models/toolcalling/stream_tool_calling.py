from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://localhost:8317/v1"
)

model_with_tool = model.bind_tools([get_weather])

# for chunk in model_with_tool.stream(
#     "What's the weather like in New York?"
# ):
#     # Tool call chunks arrive progressively
#     for tool_chunk in chunk.tool_call_chunks:
#         if name := tool_chunk.get("name"):
#             print(f"Tool: {name}")
#         if id_ := tool_chunk.get("id"):
#             print(f"ID: {id_}")
#         if args := tool_chunk.get("args"):
#             print(f"Args: {args}")

# Accumulate tool calls
gathered = None
for chunk in model_with_tool.stream(
    "What's the weather like in New York?"
):
    gathered = chunk if gathered is None else gathered + chunk
    print(gathered.tool_calls)