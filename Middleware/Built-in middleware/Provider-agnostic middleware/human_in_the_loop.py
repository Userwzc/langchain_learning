# 在工具调用执行前暂停智能体的运行，以供人工审批、编辑或拒绝这些调用。
# Human-in-the-loop适用于以下场景：
# 需要人工审批的高风险操作（例如数据库写入、金融交易）。
# 需要人工监督的合规工作流程。
# 长时间运行的对话，其中人类反馈引导智能体。
# API reference: HumanInTheLoopMiddleware
# ！Human-in-the-loop middleware requires a checkpointer to maintain state across interruptions

from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("GOOGLE_API_KEY") 

def read_email_tool(email_id: str) -> str:
    """Mock function to read an email by its ID."""
    return f"Email content for ID: {email_id}"

def send_email_tool(recipient: str, subject: str, body: str) -> str:
    """Mock function to send an email."""
    return f"Email sent to {recipient} with subject '{subject}'"

model = ChatGoogleGenAI(
    model="gemini-2.5-flash",
    base_url="http://localhost:8317"
)

agent = create_agent(
    model = model,
    tools = [read_email_tool, send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email_tool": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "read_email_tool": False  # auto-approve this tool ,True means all decisions are allowed: approve, edit, reject
            }
        )
    ]
)