# 为智能体配备任务规划与跟踪能力，以应对复杂的多步骤任务。
# 待办事项清单适用于以下场景：
# 需要协调多个工具的复杂多步骤任务。
# 长时间运行的操作，其中进度可见性很重要。
# This middleware automatically provides agents with a `write_todos` tool and system prompts to guide effective task planning.

# API reference: TodoListMiddleware
# params:
# system_prompt: string 用于指导待办事项使用的自定义系统提示。若未指定，则使用内置提示
# tool_description: string 
# `write_todos` 工具的自定义描述，若未指定，则使用内置描述

# from langchain.agents import create_agent
# from langchain.agents.middleware import TodoListMiddleware

# agent = create_agent(
#     model="gpt-4o",
#     tools=[read_file, write_file, run_tests],
#     middleware=[TodoListMiddleware()],
# )


