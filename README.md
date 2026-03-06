[English](README.md) | [简体中文](README_zh.md)

# 🦜🔗 LangChain & LangGraph Practice Workspace

This repository is my dedicated sandbox for learning and experimenting with **LangChain** and **LangGraph**. It contains scripts, mini-projects, and component tests aimed at mastering the orchestration of Large Language Models (LLMs).

## 🚀 What's Inside?

- **Agent Basics**: Scripts initializing and configuring chat models, defining system prompts, and creating basic tools (e.g., weather APIs).
- **Memory Management**: Implementations of Short-term Memory (`InMemorySaver`) to maintain conversational state across multi-turn interactions.
- **Structured Output**: Experiments with constraining LLM responses to specific schemas using `pydantic` and dataclasses.
- **Custom Tools & Middlewares**: Designing custom functions, integrating runtime contexts (`ToolRuntime`), and managing agent routing logic and state transitions.
- **LangGraph Workflows**: Building directed acyclic graphs (DAGs) to define complex, multi-step agentic behaviors and human-in-the-loop processes.

## 🛠️ Technologies Explored
- `langchain` & `langchain-core`
- `langgraph`
- `openai` / `deepseek` APIs
- `pydantic` & Dataclasses
- Asynchronous execution (`asyncio`)

## 🎯 Goal
To transition from writing simple single-prompt scripts to architecting robust, stateful, and autonomous AI agents capable of handling complex reasoning and multi-step tasks.
