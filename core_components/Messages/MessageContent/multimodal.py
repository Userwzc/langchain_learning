from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from dotenv import load_dotenv  
import os
import base64
load_dotenv()
os.getenv("OPENAI_API_KEY") 

model  = init_chat_model(
    model = "gpt-5.1",
    base_url = "http://localhost:8317/v1"
)

message = HumanMessage(content=[
    {"type": "text", "text": "描述一下这张图片的内容。"},
    {
        "type": "image",
        "base64": base64.b64encode(open("core_components/Messages/MessageContent/allmetric.png", "rb").read()).decode("utf-8"),
        "mime_type": "image/png"
    }
])

response = model.invoke([message])
print(response.text)