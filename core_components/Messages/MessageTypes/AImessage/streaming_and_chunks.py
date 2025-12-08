from langchain.messages import SystemMessage,HumanMessage,AIMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv  
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

model  = init_chat_model(
    model = "gpt-5.1",
    base_url = "http://localhost:8317/v1"
)

# 在流式传输过程中，您将收到可以组合成一个完整消息对象的AIMessageChunk对象：
chunks = []
full_message = None
for chunk in model.stream("Hi"):
    chunks.append(chunk)
    print(type(chunk))  #<class 'langchain_core.messages.ai.AIMessageChunk'>
    full_message = chunk if full_message is None else full_message + chunk
# 最终，您将获得一个完整的AIMessage对象：
print(full_message)  
print(type(full_message))  # <class 'langchain_core.messages.ai.AIMessage'>