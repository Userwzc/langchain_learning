# 提供对文件系统的 Glob 和 Grep 搜索工具。
# 文件搜索中间件适用于以下场景：
# 代码探索与分析
# 通过文件名模式查找文件
# 使用正则表达式搜索代码内容
# 需要进行文件发现的大型代码库

# API reference: FileSystemFileSearchMiddleware
# params:
# root_path: str (required)  要搜索的根目录。所有文件操作都相对于此路径进行。

# use_ripgrep: bool  default:"True"
# 是否使用 ripgrep 进行搜索。如果 ripgrep 不可用，则回退到 Python 正则表达式。

# max_file_size_mb: int  default:"10"
# 要搜索的文件最大大小（以 MB 为单位）。超过此大小的文件将被跳过。


# The middleware adds two search tools to agents:
# Glob tool: 快速文件模式匹配
# Supports patterns like **/*.py , src/**/*.ts
# 返回按修改时间排序的匹配文件路径

# Grep tool: 使用正则表达式进行内容搜索
# 完整支持正则表达式语法
# 使用 include 参数按文件模式进行过滤
# 三种输出模式：files_with_matches、content、count

from langchain.agents import create_agent
from langchain.agents.middleware import FilesystemFileSearchMiddleware
from langchain.messages import HumanMessage

agent = create_agent(
    model = "gpt-4o",
    tools = [],
    middleware = [
        FilesystemFileSearchMiddleware(
            root_path="/workspace",
            use_ripgrep=True,
            max_file_size_mb=10
        )
    ]
)

# Agent can now use glob_search and grep_search tools 
result = agent.invoke({
    "messages": [HumanMessage("Find all Python files containing 'async def'")]
})

# The agent will use:
# 1. glob_search(pattern="**/*.py") to find Python files
# 2. grep_search(pattern="async def", include="*.py") to find async functions