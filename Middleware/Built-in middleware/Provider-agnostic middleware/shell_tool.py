# 向智能体暴露一个持久的 Shell 会话以执行命令。
# Shell 工具中间件适用于以下场景：
# 智能体需要执行系统命令
# 开发与部署自动化任务
# 测试与验证工作流
# 文件系统操作与脚本执行

# 安全注意事项 ：使用适当的执行策略（HostExecutionPolicy、DockerExecutionPolicy 或 CodexSandboxExecutionPolicy）以满足您部署环境的安全要求。
# 限制 ：持久化 Shell 会话目前不支持中断（人工介入）。我们预计未来会增加对此功能的支持

# API reference: ShellToolMiddleware
# params:
# workspace_root: str | Path | None
# Shell 会话的基目录。如果省略，代理启动时会创建一个临时目录，并在结束时将其删除。

# startup_commands: tuple[str, ...] | list[str] | str | None
# 会话启动后按顺序执行的可选命令

# shutdown_commands: tuple[str, ...] | list[str] | str | None
# 在会话关闭前执行的可选命令

# execution_policy: BaseExecutionPolicy | None
# 执行策略，用于控制超时、输出限制和资源配置。选项：
# HostExecutionPolicy - 完全主机访问权限（默认）；最适合受信任的环境，例如代理已运行在容器或虚拟机内部的情况
# DockerExecutionPolicy - 为每次代理运行启动一个独立的 Docker 容器，提供更强的隔离性
# CodexSandboxExecutionPolicy - 复用 Codex CLI 沙箱，以施加额外的系统调用/文件系统限制

# redaction_rules: tuple[RedactionRule, ...] | list[RedactionRule] | None
# 可选的脱敏规则，用于在将命令输出返回给模型之前对其进行清理

# tool_description: str | None
# 可选的已注册 shell 工具描述覆盖

# shell_command: Sequence[str] | str | None
# 可选的 shell 可执行文件（字符串）或用于启动持久会话的参数序列。默认为 /bin/bash

# env: Mapping[str, Any] | None
# 可选的环境变量，用于提供给 shell 会话。在命令执行前，值会被强制转换为字符串

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ShellToolMiddleware,
    HostExecutionPolicy,
    DockerExecutionPolicy,
    RedactionRule
)

# Basic shell tool with host execution
agent = create_agent(
    model = "gpt-4o",
    tools = ["search_tool"],
    middleware=[
        ShellToolMiddleware(
            workspace_root= "/workspace",
            execution_policy= HostExecutionPolicy(),
        )
    ]
)

# Docker isolation with startup commands
agent_docker = create_agent(
    model = "gpt-4o",
    tools = [],
    middleware=[
        ShellToolMiddleware(
            workspace_root= "/workspace",
            startup_commands= ["pip install requests", "export PYTHONPATH=/workspace"],
            execution_policy= DockerExecutionPolicy(
                image="python:3.11-slim",
                command_timeout=60.0,
            )
        )
    ]
)

# With output redaction
agent_redacted = create_agent(
    model = "gpt-4o",
    tools = [],
    middleware=[
        ShellToolMiddleware(
            workspace_root= "/workspace",
            redaction_rules= [
                RedactionRule(pii_type="api_key", detector=r"sk-[a-zA-Z0-9]{32}"),
            ]
        )
    ]
)
