# Personal Identifiable Information (PII)
# 使用可配置的策略检测并处理对话中的个人身份信息（PII）。
# PII 检测适用于以下场景：
# 具有合规要求的医疗和金融应用
# 需要清理日志的客户服务代理
# 任何处理敏感用户数据的应用程序

# API reference: PIIMiddleware
# params:
# pii_type : string (required) 
# 要检测的 PII 类型。可以是内置类型（email、credit_card、ip、mac_address、url）或自定义类型名称。

# strategy : string  default : "redact"
# 如何处理检测到的个人身份信息（PII）。选项：
# 'block': 检测到时抛出异常
# 'redact': 替换为 [REDACTED_{PII_TYPE}]    
# 'mask': 部分遮蔽（例如：****-****-****-1234）
# 'hash': 替换为确定性哈希值

# detector : function | regex
# 自定义检测器函数或正则表达式模式。若未提供，则使用该 PII 类型的内置检测器。

# apply_to_input: boolean  default : "True"
# 在模型调用前检查用户消息

# apply_to_output: boolean  default: "False"
# 在模型调用后检查 AI 消息

# apply_to_tool_results: boolean  default: "False"
# 执行后检查工具结果消息

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
import re

# Method 1: Regex pattern string
agent1 = create_agent(
    model = 'gpt-4o',
    tools = [],
    middleware = [
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block"
        )
    ]
)

# Method 2: Compiled regex pattern
agent2 = create_agent(
    model = 'gpt-4o',
    tools = [],
    middleware= [
        PIIMiddleware(
            "phone_number",
            detector=re.compile(r"\+?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{4}"),
            strategy="mask"
        )
    ]
)

# Method 3：Custom detector function
def detect_ssn(content: str) ->list[dict[str, str | int]]:
    """Detect SSN with validation.
    
    Returns a list of dictionaries with 'text', 'start', and 'end' keys.
    """
    matches = []
    pattern = r"\d{3}-\d{2}-\d{4}"
    for match in re.finditer(pattern, content):
        ssn = match.group(0)
        # Validate: first 3 digits shouldn't be 000, 666, or 900-999
        first_three = int(ssn[:3])
        if first_three not in [0, 666] and not (900 <= first_three <= 999):
            matches.append({
                "text": ssn,
                "start": match.start(),
                "end": match.end()
            })
    return matches
# 检测器函数必须接受一个字符串（内容）并返回匹配结果：
# def detector(content: str) -> list[dict[str, str | int]]:
#     return [
#         {"text": "matched_text", "start": 0, "end": 12},
#         # ... more matches
#     ]

agent3 = create_agent(
    model="gpt-4o",
    tools=[],
    middleware=[
        PIIMiddleware(
            "ssn",
            detector=detect_ssn,
            strategy="hash",
        ),
    ],
)