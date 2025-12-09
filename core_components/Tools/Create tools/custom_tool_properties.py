from langchain.tools import tool

# Custom tool name
# 默认情况下，工具名称来自函数名称。当你需要更具描述性的名称时，可以对其进行覆盖

@tool("web_search") # Custom name
def search(query: str) -> str:
    """Search the web for information related to the query.

    Args:
        query (str): The search terms to look for
    Returns:
        str: A summary of the search results
    """
    return f"Results for '{query}'"

print(search.name)  # Output: web_search

# Custom tool description
# 覆盖自动生成的工具描述，以提供更清晰的模型指引：
@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Calculate the result of a mathematical expression.

    Args:
        expression (str): The mathematical expression to evaluate
    Returns:
        str: The result of the calculation
    """
    return str(eval(expression))