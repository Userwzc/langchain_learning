from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage, AIMessage

import os
load_dotenv()
os.getenv("DEEPSEEK_API_KEY")


model = init_chat_model(
    "deepseek-chat"
)

# response = model.invoke("Why do parrots have colorful feathers?")

# print(response)

# conversation = [
#     {"role": "system", "content": "You are a helpful assistant that translates English to French."},
#     {"role": "user", "content": "Translate: I love programming."},
#     {"role": "assistant", "content": "J'adore la programmation."},
#     {"role": "user", "content": "Translate: I love building applications."}
# ]

conversation = [
    SystemMessage(content="You are a helpful assistant that translates English to French."),
    HumanMessage(content="Translate: I love programming."),
    AIMessage(content="J'adore la programmation."),
    HumanMessage(content="Translate: I love building applications.")
]

response = model.invoke(conversation)

print(response)