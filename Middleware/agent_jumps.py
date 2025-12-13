# 要提前退出中间件，请返回一个包含`jump_to`的字典
# Available jump targets:
# 'end' : 跳转到代理执行的末尾（或第一个 after_agent 钩子）
# 'tools': 跳转到工具节点
# 'model': 跳转到模型节点（或第一个 before_model 钩子）

# Example
# Decorator
from langchain.agents.middleware import after_model, hook_config, AgentState
from langchain.messages import AIMessage
from langgraph.runtime import Runtime
from typing import Any

@after_model
@hook_config(can_jump_to=['end'])
def check_for_blocked(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    last_message = state['messages'][-1]
    if "BLOCKED" in last_message.content:
        return {
            "messages": [AIMessage("I cannot respond to that request.")],
            "jump_to": "end"
        }
    return None

# Class
from langchain.agents.middleware import AgentMiddleware

class BlockedContentMiddleware(AgentMiddleware):

    @hook_config(can_jump_to=['end'])
    def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        last_message = state['messages'][-1]
        if "BLOCKED" in last_message.content:
            return {
                "messages": [AIMessage("I cannot respond to that request.")],
                "jump_to": "end"
            }
        return None
    