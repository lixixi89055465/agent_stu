from fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent

from agent.tools.tool_demo7 import zhipuai_client

server = FastMCP(name='python_mcp',instructions='老肖的Python代码实现MCP服务器')


@server.tool(name='zhipuai_search')
def my_search(query: str) -> str:
    """搜索互联网上的内容，包括实时天气等"""
    try:
        print('执行我的python 工具，输入的参数为:', query)
        response = zhipuai_client.web_search.web_search(
            search_engine='search_pro',
            search_query=query,
        )
        if response.search_result:
            return '\n\n'.join([d.content for d in response.search_result])
        return '没有搜索到任何内容!'
    except Exception as e:
        print(e)
        return '没有搜索到任务内容!'


@server.tool(name="say_hello")
def say_hello(username: str) -> str:
    '''给指定的用户打个招呼'''
    return f"{username}你好啊"


@server.prompt
def ask_about_topic(topic: str) -> str:
    '''生成请求解释特定主题的用户消息模板'''
    return f'能否请您解释一下{topic} ，这个概念'


# 高级提示模板
@server.prompt
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    '''生成代码编写请求的用户消息模板'''
    content = f'请用{language}编写一个实现以下功能的函数{task_description}'
    return PromptMessage(
        role='user',
        content=TextContent(type='text', text=content)
    )


# 结构化资源：自动序列化字典为JSON
@server.resource('resource://config')
def get_config() -> dict:
    '''以JSON格式返回应用的配置'''
    return {
        'theme': 'dark',
        'version': '1.2.0',
        'features': ['tools', 'resources']
    }
