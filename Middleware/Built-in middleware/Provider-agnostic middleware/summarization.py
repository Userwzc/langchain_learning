# 当接近令牌限制时，自动汇总对话历史，在保留近期消息的同时压缩较早的上下文。
# 摘要功能适用于以下场景：
# - 超出上下文窗口长度的长时间对话
# - 具有丰富历史记录的多轮对话
# - 需要保留完整对话上下文的应用场景

# API reference: SummarizationMiddleware
# params：
# model: String | BaseChatModel (required) - 用于生成摘要的模型
# trigger : ContextSize | list[ContextSize] | None
# 触发摘要的条件，可以是：
# 一个单一的 ContextSize 字典（必须满足所有属性，AND）
# 一个 ContextSize 字典列表（满足任一条件即可，OR）
# Each condition can include:
# `fraction` : 模型上下文长度的占比（0-1）
# `tokens`： 绝对令牌数量
# `messages`: 消息数量
# 每个条件必须至少指定一个属性。如果未提供，将不会自动触发摘要生成。

# keep: ContextSize  default: {"messages": 20}
# 摘要后要保留多少上下文。请明确指定以下选项中的一个：
# `fraction` : 模型上下文长度的占比（0-1）
# `tokens`： 绝对令牌数量
# `messages`: 保留的最近消息数量

# token_counter: function
# 自定义的 token 计数函数。默认采用基于字符的计数方式。

# summary_prompt: string
# 用于摘要的自定义提示模板。若未指定，则使用内置模板。该模板应包含 {messages} 占位符，用于插入对话历史。

# trim_tokens_to_summarize: number  default: 4000
# 生成摘要时包含的最大 token 数量。在进行摘要前，消息将被裁剪以适应此限制。

# summary_prefix: string
# 要添加到摘要消息前的前缀。如果未提供，则使用默认前缀。

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_google_genai import ChatGoogleGenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenAI(
    model="gemini-2.5-flash",
    base_url="http://localhost:8317"
)

# Single condition: trigger if tokens >= 4000 or messages >= 10
agent = create_agent(
    model = model,
    tools = [],
    middleware=[
        SummarizationMiddleware(
            model = model,
            trigger = [("tokens", 4000),("messages", 10)],
            keep = ("messages", 20)
        )]
)

# Using fractional limits
agent2 = create_agent(
    model="gpt-4o",
    tools=[],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=("fraction", 0.8),
            keep=("fraction", 0.3),
        ),
    ],
)