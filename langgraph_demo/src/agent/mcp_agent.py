import asyncio
import logging

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from agent.env_utils import ZHIPU_API_KEY
from agent.models import search_tool, llm

python_mcp_server_config = {
    'url': 'http://127.0.0.1:8080/sse',
    'transport': 'sse',
}
zhipuai_mcp_server_config = {
    'url': f'https://open.bigmodel.cn/api/mcp/web_search/sse?Authorization={ZHIPU_API_KEY}',
    'transport': 'sse'
}
mcp_client = MultiServerMCPClient(
    {
        # 'python_mcp': python_mcp_server_config,
        'zhipuai_mcp': zhipuai_mcp_server_config
    }
)


async def create_agent():
    '''必须是异步函数中'''
    mcp_tools = await mcp_client.get_tools()
    print(mcp_tools)
    # p = await mcp_client.get_prompt(server_name='python_mcp',
    #                                 prompt_name='ask_about_topic',
    #                                 arguments={'topic': '深度学习'})
    # print(p)
    # data = await mcp_client.get_resources(server_name='python_mcp',
    #                                       uris='resource://config')
    # print(data)

    return create_react_agent(
        llm,
        tools=mcp_tools,
        prompt='你是一个智能助手，尽可能的调用工具回答用户的逻辑'
    )


agent = asyncio.run(create_agent())
