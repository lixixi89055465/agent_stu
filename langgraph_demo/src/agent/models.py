from typing import Type

from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from zai import ZhipuAiClient

from agent.env_utils import ALIBABA_API_KEY, ALIBABA_BASE_URL, ZHIPU_API_KEY

class SearchArgs(BaseModel):
    query: str = Field(description="需要进行网络搜索的信息.")


# 网络搜索的工具
class MySearchTool(BaseTool):
    # 工具名字
    name: str = 'search_tool'
    description: str = '搜索互联网上公开内容的工具'
    return_direct: bool = False
    args_schema: Type[BaseModel] = SearchArgs

    def _run(self, query) -> str:
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

llm = ChatOpenAI(
    model='qwen-turbo',
    temperature=0.8,
    # api_key="XX",
    api_key=ALIBABA_API_KEY,
    # base_url='http://localhost:6006/v1',
    base_url=ALIBABA_BASE_URL,
    extra_body={'chat_template_kwargs': {'enable_thinking': False}}
)
search_tool = MySearchTool()
zhipuai_client = ZhipuAiClient(api_key=ZHIPU_API_KEY)
