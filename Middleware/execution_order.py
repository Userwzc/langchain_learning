# 使用多个中间件时，需要了解它们的执行方式：
# agent = create_agent(
#     model="gpt-4o",
#     middleware=[middleware1, middleware2, middleware3],
#     tools=[...],
# )

# Execution flow

# Before hooks run in order:
# 1. middleware1.before_agent()
# 2. middleware2.before_agent()
# 3. middleware3.before_agent()

# Agent loop starts
# 4. middleware1.before_model()
# 5. middleware2.before_model()
# 6. middleware3.before_model()

# Wrap hooks nest like function calls:
# 7. middleware1.wrap_model_call() -> middleware2.wrap_model_call() -> middleware3.wrap_model_call() -> model

# After hooks run in reverse order:
# 8. middleware3.after_model()
# 9. middleware2.after_model()
# 10. middleware1.after_model()

# Agent loop ends
# 11. middleware3.after_agent()
# 12. middleware2.after_agent()
# 13. middleware1.after_agent()


# key rules：
# before_* hooks : First to last
# after_* hooks : Last to first(reverse)
# wrap_* hooks : Nested (first middleware wraps all others)