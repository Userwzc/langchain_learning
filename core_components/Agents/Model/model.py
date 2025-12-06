from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

# Dynamic models are selected at runtime based on the current state and context. 
# This enables sophisticated routing logic and cost optimization.

basic_model = ChatDeepSeek(
    model = "deepseek-chat"
)

reasoner_model = ChatDeepSeek(
    model = "deepseek-reasoner"
)

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

    if message_count > 10:
        model = reasoner_model
    else:
        model = basic_model

    return handler(request.override(model=model))

agent = create_agent(
    model = basic_model, # default model
    middleware=[dynamic_model_selection]
)

# 在使用结构化输出时，不支持预绑定模型（已经调用过bind_tools的模型）。
# 如果您需要在使用结构化输出时进行动态模型选择，请确保传递给中间件的模型不是预绑定的。
