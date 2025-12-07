from langchain_openai import ChatOpenAI
from dotenv import load_dotenv  
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://localhost:8317/v1",
)

tool = {"type": "web_search"}

model_with_tool = model.bind_tools([tool])

response = model_with_tool.invoke("What was a positive news story from today?")
print(response.content_blocks)