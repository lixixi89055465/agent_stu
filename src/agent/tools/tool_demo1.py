from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from langchain_core.tools import tool
from langchain_core.utils.function_calling import tool_example_to_messages
from pydantic import BaseModel, Field

from agent.my_llm import zhipuai_client


@tool('my_web_search', parse_docstring=True)
def web_search(query: str) -> str:
    '''
    互联网搜索的工具，可以搜索所有公开的信息。
    Args:
        qury:需要进行互联网查询的信息。
    Returns:
        返回搜索的结果信息，该信息是一个文本字符串
    '''
    try:
        resp = zhipuai_client.web_search.web_search(
            search_engine='search_pro',
            search_query=query
        )
        if resp.search_result:
            return '\n\n'.join([d.content for d in resp.search_result])
        return '没有搜索到任何结果'

    except Exception as e:
        print(e)
        return f'Error :{e}'


class SearchArgs(BaseModel):
    query: str = Field(..., description='需要尽心互联网查询的查询信息')
    second: int = Field(..., description='第二个参数')


@tool('my_web_search', args_schema=SearchArgs, description='互联网搜索的工具，可以搜索所有公开的信息')
def web_search2(query: str) -> str:
    pass
