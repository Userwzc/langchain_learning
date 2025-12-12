# 限制模型调用次数，以防止无限循环或产生过高成本。模型调用限制适用于以下场景：
# 防止失控的智能体发起过多的 API 调用。
# 对生产环境部署实施成本控制。
# 在特定调用预算内测试智能体行为。
# API reference: ModelCallLimitMiddleware
# params:
# thread_limit: number  一个线程中所有运行的最大模型调用次数。默认无限制。
# run_limit: number  单次invoke的最大模型调用次数。默认无限制。
# exit_behavior: string  default: 'end'
# 达到限制时的行为。选项：'end'（优雅终止）或 'error'（抛出异常）

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware

agent = create_agent(
    model="gpt-4o",
    tools=[],
    middleware=[
        ModelCallLimitMiddleware(
            thread_limit=10,
            run_limit=5,
            exit_behavior="end",
        ),
    ],
)