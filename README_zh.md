[English](README.md) | [简体中文](README_zh.md)

# 🦜🔗 LangChain & LangGraph 框架实践工作区

本仓库是用于学习和试验 **LangChain** 与 **LangGraph** 的专属沙盒。包含各种脚本、微型项目和组件测试，旨在掌握大语言模型的复杂编排与调度技术。

## 🚀 核心内容

- **智能体基础 (Agent Basics)**: 初始化与配置聊天模型、定义系统 Prompt，以及构建基础工具（如天气 API 调用）的脚本。
- **记忆管理 (Memory Management)**: 实现短期记忆机制 (`InMemorySaver`)，以在多轮交互中持续维护对话状态。
- **结构化输出 (Structured Output)**: 使用 `pydantic` 和数据类约束大模型输出特定格式数据的实验验证。
- **自定义工具与中间件 (Custom Tools & Middlewares)**: 设计自定义工具，集成运行时上下文 (`ToolRuntime`)，以及管理智能体的路由逻辑和状态转换。
- **LangGraph 工作流 (LangGraph Workflows)**: 构建有向无环图 (DAG) 以定义复杂的多步智能体行为及 Human-in-the-loop (人在回路) 流程。

## 🛠️ 技术栈
- `langchain` & `langchain-core`
- `langgraph`
- `openai` / `deepseek` APIs
- `pydantic` & 数据类 (Dataclasses)
- 异步编程执行 (`asyncio`)

## 🎯 目标愿景
从编写简单的单提示词脚本，进阶到具备架构高鲁棒性、有状态且能自主处理复杂推理与多步任务的 AI 智能体系统的能力。
