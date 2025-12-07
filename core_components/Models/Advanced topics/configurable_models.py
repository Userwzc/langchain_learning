# 你也可以通过指定 configurable_fields 来创建一个运行时可配置的模型。
# 如果你未指定模型值，那么 'model' 和 'model_provider' 将默认为可配置。
from langchain.chat_models import init_chat_model

configurable_model = init_chat_model(temperature=0)

configurable_model.invoke(
    "what's your name?",
    config = {"configurable": {"model": "gpt-5"}}  # run with gpt-5
)

configurable_model.invoke(
    "what's your name?",
    config = {
        "configurable": {
            "model": "gpt-5.1"  # run with gpt-5.1
        }
    }
)


# configurable model with default values
# 我们可以创建一个具有默认模型值的可配置模型，指定哪些参数是可配置的，并为可配置参数添加前缀
first_model =init_chat_model(
    model="gpt-5",
    temperature = 0,
    configurable_fields=("model","model_provider","temperature","max_tokens"),
    config_prefix="first"
)
first_model.invoke(
    "what's your name?"
)
first_model.invoke(
    "what's your name?",
    config = {
        "configurable": {
            "first_model": "gpt-5.1",  # run with gpt-5.1
            "first_temperature": 0.7,
            "first_max_tokens": 150
        }
    }
)