import asyncio

from langchain.agents import create_agent
from agent.my_llm import llm
from agent.tools.tool_demo1 import web_search


# async def my_create_agent():
#     return create_agent(
#         llm,
#         tools=[web_search],
#         system_prompt="你是一个智能助手,尽可能的调用工具回答用户的问题"
#     )
#
#
# my_agent = asyncio.run(my_create_agent())

agent=create_agent(
        llm,
        tools=[web_search],
        system_prompt="你是一个智能助手,尽可能的调用工具回答用户的问题"
    )
agent.ainvoke()

