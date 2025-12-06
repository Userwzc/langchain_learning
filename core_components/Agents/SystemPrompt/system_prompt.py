from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage

# 你可以通过提供提示来塑造你的代理如何处理任务。system_prompt参数可以作为字符串提供
# 如果没有提供，agent将从消息中直接推断其任务
# system_prompt 参数可以接受一个str,或者是SystemMessage对象
# SystemMessage可以让你对提示结构有更多的控制，这对于像Anthropic的提示缓存这样的特定提供者功能很有用


literary_agent = create_agent(
    model = "anthropic:claude-sonnet-4-5",
    system_prompt=SystemMessage(
        content = [
            {
                "type": "text",
                "text": "You are an AI assistant tasked with analyzing literary works."
            },
            {
                "type": "text",
                "text": "<the entire contents of 'Pride and Prejudice'>",
                "cache_control": {"type": "ephemeral"}
            }
        ]
    )
)

# 带有{"type": "ephemeral"}的cache_control字段告诉Anthropic缓存该内容块，从而减少使用相同系统提示的重复请求的延迟和成本。

result = literary_agent.invoke(
    {"messages": [HumanMessage(content="Analyze the major themes in 'Pride and Prejudice'.")]}
)