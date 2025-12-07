from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("DEEPSEEK_API_KEY")

model = init_chat_model(
    "deepseek-chat"
)

# 本节描述了一个聊天模型方法batch()，该方法在客户端并行化模型调用。
# 它与由推理提供者（如OpenAI或Anthropic）支持的批量API不同。
# responses = model.batch(
#     [
#         "What is the capital of China?",
#         "What is the capital of France?",
#         "Explain the theory of relativity in simple terms."
#     ]
# )

# for response in responses:
#     print(response)

# 默认情况下， batch() 仅会返回整个批次的最终输出。
# 如果你想在每个单独输入生成完成时就立即收到其输出，可以使用 batch_as_completed() 来流式传输结果：
for response in model.batch_as_completed(
    [
        "What is the capital of China?",
        "What is the capital of France?",
        "Explain the theory of relativity in simple terms."
    ]
):
    print(response)
# 使用 batch_as_completed() 时，结果可能会乱序到达。每个结果都包含输入索引，以便按需匹配并重建原始顺序。

# 在使用 batch() 或 batch_as_completed() 处理大量输入时，你可能希望控制最大并行调用数量。
# 这可以通过在 RunnableConfig 字典中设置 max_concurrency 属性来实现。
# model.batch(
#     list_of_inputs,
#     config={
#         'max_concurrency': 5,  # Limit to 5 parallel calls
#     }
# )