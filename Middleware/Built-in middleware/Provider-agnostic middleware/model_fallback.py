# Model fallback
# 当主模型失败时，自动回退到备用模型。模型回退适用于以下场景：
# 构建能够应对模型中断的弹性智能体
# 通过回退到更便宜的模型来优化成本
# 跨 OpenAI、Anthropic 等提供商的冗余

# API reference: ModelFallbackMiddleware
# params:
# first_model: string | BaseChatModel (required)  主模型失败时首先尝试的备用模型
# *additional_models: string | BaseChatModel  如果先前的模型失败，按顺序尝试的额外备用模型
