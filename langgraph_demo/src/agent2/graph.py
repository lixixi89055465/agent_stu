from typing import TypedDict

from langgraph.graph import StateGraph


class State(TypedDict):
    joke: str  # 生成的冷笑话内容
    topic: str  # 用户指定的主题
    feedback: str  # 改进建议
    funny_or_not: str  # 幽默评级



# 构建一个工作流
builder = StateGraph(State)
builder.add_node('generator', '')
