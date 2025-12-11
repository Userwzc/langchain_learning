# `tool_message_content`参数允许你自定义在生成结构化输出时，出现在对话历史中的消息内容
from pydantic import BaseModel, Field
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("OPENAI_API_KEY")

class MeetingAction(BaseModel):
    """Action items extracted from a meeting transcript."""
    task: str = Field(description="The specific task to be completed")
    assignee: str = Field(description="Person responsible for the task")
    priority: Literal["low", "medium", "high"] = Field(description="Priority level")

model = ChatOpenAI(
    model = "gemini-2.5-flash",
    base_url="http://localhost:8317/v1"
)

agent = create_agent(
    model = model,
    response_format=ToolStrategy(
        schema=MeetingAction,
        tool_message_content = "Action item captured and added to meeting notes!"
    )
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "From our meeting: Sarah needs to update the project timeline as soon as possible"}]
})

for message in result["messages"]:
    message.pretty_print()