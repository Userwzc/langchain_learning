# 许多模型能够通过多步推理得出结论。这涉及到将复杂问题分解成更小、更易于管理的步骤。
# 如果底层模型支持，你可以展示这个推理过程，以便更好地理解模型是如何得出最终答案的。

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv  
import os
load_dotenv()
os.getenv("OPENAI_API_KEY") 
model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://localhost:8317/v1",
    reasoning = {
        "effort": "medium",
        "summary": "auto"
    }
)

response = model.invoke("一块巧克力重240g,如果我每天吃一半，多少天后我会吃完？")

print(response.text)
print("Reasoning steps:")
for block in response.content_blocks:
    if block["type"] == "reasoning":
        print(block["reasoning"])