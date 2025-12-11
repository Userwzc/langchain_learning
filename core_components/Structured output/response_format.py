# 结构化输出允许智能体以特定且可预测的格式返回数据。
# 与解析自然语言响应不同，您将直接获得 JSON 对象、Pydantic 模型或数据类形式的结构化数据，供您的应用程序直接使用。

# LangChain的`create_agent`能自动处理结构化输出。
# 用户设置所需的结构化输出模式后，当模型生成结构化数据时，该数据会被捕获、验证，并返回在代理状态的`structured_response`键中

# def create_agent(
#     ...
#     response_format: Union[
#         ToolStrategy[StructuredResponseT],
#         ProviderStrategy[StructuredResponseT],
#         type[StructuredResponseT],
#     ]

# ToolStrategy[StructuredResponseT] ：使用工具调用以生成结构化输出
# ProviderStrategy[StructuredResponseT] ：使用提供商原生的结构化输出
# type[StructuredResponseT]：模式类型——根据模型能力自动选择最佳策略
# None :不使用结构化输出

# 当直接提供 schema 类型时，LangChain 会自动选择：
# ProviderStrategy（如果提供商支持结构化输出）
# ToolStrategy（否则）
# 如果使用 langchain>=1.1，对原生结构化输出特性的支持会从模型的配置文件数据中动态读取。
# 如果数据不可用，请使用其他条件或手动指定：
# custom_profile = {
#     "structured_output": True,
#     # ...
# }
# model = init_chat_model("...", profile=custom_profile)
# 如果指定了工具，则模型必须支持同时使用工具和结构化输出。