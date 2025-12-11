# Langchain的流式传输系统可让你将代理运行过程中的实时反馈呈现到你的应用程序中
# 使用Langchain流失传输可以实现的功能：
# Stream agent progress 在每个代理步骤后获取状态更新
# Stream LLM tokens  在语言模型生成令牌时进行流式传输
# Stream custom updates  发出用户定义的信号
# Stream multiple modes  可选择 updates（智能体进度）、messages（LLM 令牌及元数据）或 custom（任意用户数据）

# Supported stream modes:
# 将以下一个或多个流模式以列表形式传递给`stream`或`astream`方法：
# `updates` : 在每个智能体步骤之后流式传输状态更新。如果在同一步骤中进行了多次更新（例如，运行了多个节点），这些更新将分别进行流式传输。
# `messages`: 从任何调用 LLM 的图节点中流式传输 (token, metadata) 元组。
# `custom`： 使用stream writer从图节点内部流式传输自定义数据。