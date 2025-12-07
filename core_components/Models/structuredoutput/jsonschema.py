from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os    
import json   
load_dotenv()
os.getenv("OPENAI_API_KEY")

json_schema = {
    "title": "Movie",
    "description": "A movie with details",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "The title of the movie"
        },
        "year": {
            "type": "integer",
            "description": "The year the movie was released"
        },
        "director": {
            "type": "string",
            "description": "The director of the movie"
        },
        "rating": {
            "type": "number",
            "description": "The movie's rating out of 10"
        }
    },
    "required": ["title", "year", "director", "rating"]
}

model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://localhost:8317/v1"
)

# model_with_structure = model.with_structured_output(json_schema,method = 'json_schema')
# # Method parameter : Some providers support different methods ('json_schema', 'function_calling', 'json_mode')
# # 'json_schema' 通常指的是提供方提供的专用结构化输出功能
# # 'function_calling' 通过强制按照给定模式调用工具来生成结构化输出。
# # 'json_mode' 是一些提供方提供的 'json_schema' 的前身 - 它生成有效的 JSON，但模式必须在提示中描述

# # include_raw = True 会包含原始AIMessage响应
# # model_with_structure = model.with_structured_output(Movie, include_raw=True)

# response = model_with_structure.invoke("Provide details about the movie Inception.")
# print(response)
