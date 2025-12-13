# Decorator
from langchain.agents.middleware import warp_model_call, ModelRequest, ModelResponse
from typing import Callable
from langchain.chat_models import init_chat_model

complex_model = init_chat_model("gpt-4o")
simple_model = init_chat_model("gpt-4o-mini")

@warp_model_call
def dynamic_model_selector(
    request:ModelRequest,
    handler:Callable[[ModelRequest],ModelResponse]
) -> ModelResponse:
    # Use different model based on conversation length
    if len(request.messages) > 10:
        model = complex_model
    else:
        model = simple_model
    return handler(request.override(model=model))

# Class
from langchain.agents.middleware import AgentMiddleware

class DynamicModelSelectionMiddleware(AgentMiddleware):
    def warp_model_call(
        self,
        request:ModelRequest,
        handler:Callable[[ModelRequest],ModelResponse]
    ) -> ModelResponse:
        # Use different model based on conversation length
        if len(request.messages) > 10:
            model = complex_model
        else:
            model = simple_model
        return handler(request.override(model=model))