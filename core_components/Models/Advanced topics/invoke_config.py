# 在调用模型时，您可以通过RunnableConfig字典使用config参数传递额外的配置。
# 这提供了对执行行为、回调和元数据跟踪的运行时控制。

# response = model.invoke(
#     "Tell me a joke",
#     config={
#         "run_name": "joke_generation",      # Custom name for this run
#         "tags": ["humor", "demo"],          # Tags for categorization
#         "metadata": {"user_id": "123"},     # Custom metadata
#         "callbacks": [my_callback_handler], # Callback handlers
#     }
# )

#这些配置值在以下情况下特别有用：
# 使用LangSmith跟踪进行调试、
# 实施自定义日志记录或监控、
# 在生产中控制资源使用、
# 跨复杂管道跟踪调用