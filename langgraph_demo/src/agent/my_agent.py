from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent.env_utils import OPENAI_BASE_URL, OPENAI_API_KEY, ALIBABA_API_KEY, ALIBABA_BASE_URL
from agent.models import llm
from agent.tools.tool_demo6 import runnable_tool


def get_weather(city: str) -> str:
    '''get weather for a given city'''
    return f"It's always sunny in {city}"


myagent = create_react_agent(
    llm,
    tools=[get_weather, runnable_tool],
    prompt='你是一个智能助手，尽可能的调用工具回答用户的问题'
)
# 执行智能体，不要要严格的目录结构
# graph.invoke()
