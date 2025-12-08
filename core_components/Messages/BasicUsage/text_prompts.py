# Messages are objects that contain:
# Role - idenfies the message type (e.g., system, user)
# Content - Represents the actual content of the message (like text, images,audio,documents,etc.)
# Metadata - Opional fields such as response information,messages IDs,and token usage.

# LangChain 提供了一种标准消息类型，该类型适用于所有模型提供者，确保无论调用哪个模型，行为都保持一致。

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os 
load_dotenv()
os.getenv("OPENAI_API_KEY")

model = init_chat_model(
    model = "gpt-5.1",
    base_uerl = "http://localhost:8317/v1"
)

# system_message = SystemMessage("You are a helpful assistant.")
# human_msg = HumanMessage("Hello, how are you?")

# messages = [system_message, human_msg]
# response = model.invoke(messages) # Return AIMessage

# Text Prompts
# 文本提示是字符串，适合不需要保留对话历史的简单生成任务
response = model.invoke("Hello, how are you?")