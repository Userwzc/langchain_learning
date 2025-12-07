import asyncio
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 
load_dotenv()
os.getenv("DEEPSEEK_API_KEY")

model = init_chat_model(
    "deepseek-chat"
)

# for chunk in model.stream("Why do parrots have colorful feathers?"):
#     print(chunk.text, end="|", flush=True)

# full = None 
# for chunk in model.stream("Why do parrots have colorful feathers?"):
#     full = chunk if full is None else full + chunk
#     print(full.text)

# astream_events()
async def main():
    async for event in model.astream_events("Hello"):
        if event["event"] == "on_chat_model_start":
            print(f"Input: {event['data']['input']}")
        elif event["event"] == "on_chat_model_stream":
            print(f"Token: {event['data']['chunk'].text}")
        elif event["event"] == "on_chat_model_end":
            print(f"Full message: {event['data']['output'].text}")
        else:
            pass

asyncio.run(main())

