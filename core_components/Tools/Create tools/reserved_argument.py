# 保留参数名称
# 以下参数名称是保留的，不能用作工具参数，使用这些名称会导致运行时错误。
# config  :  保留用于在内部向工具传递RunnableConfig
# runtime  : 保留用于ToolRuntime 参数（访问状态，上下文，存储）

# 要访问运行时信息，请使用ToolRuntime参数，而不是将你自己的参数命名为config或runtime.
