from langchain.tools import tool
# 创建工具最简单的方式是使用@tool装饰器
# 默认情况下，函数的文档字符串会成为该工具的描述，帮助模型理解何时使用
# 类型提示是必需的 ，因为它们定义了工具的输入模式。文档字符串应信息明确且简洁，以帮助模型理解工具的用途。

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query (str): Search terms to look for
        limit (int, optional): Maximum number of results to return. Defaults to 10.

    Returns:
        str: A summary of the search results
    """
    return f"Found {limit} results for '{query}'"
