- Keep middleware focused - each should do one thing well
保持中间件的专注性——每个中间件应专注于做好一件事
- Handle errors gracefully - don't let middleware errors crash the agent
优雅地处理错误——不要让中间件错误导致代理崩溃
- Use appropriate hook types:
  - Node-style for sequential logic (logging, validation) 用于顺序逻辑（如日志记录、验证）的 Node 风格
  - Wrap-style for control flow (retry,fallback,caching)  用于控制流（重试、降级、缓存）的包装式中间件
- Clearly document any custom state properties  清晰记录所有自定义状态属性
- Unit test middleware independently before integrating  在集成之前，独立对中间件进行单元测试
- Consider execution order - place critical middleware first in the list  考虑执行顺序——将关键中间件放在列表的最前面
- Use built-in middleware when possible  尽可能使用内置中间件