from openai import api_key
from pydantic import BaseModel, Field

from agent.env_utils import ZHIPU_API_KEY

from zhipuai import ZhipuAI

zhipuai_client = ZhipuAI(api_key=ZHIPU_API_KEY)


class SearchArgs(BaseModel):
    query: str = Field(description="需要进行网络搜索的信息.")


# 网络搜索的工具
class MySearchTool(BaseModel):
    # 工具名字
    name = 'search_tool'
    description = '搜索互联网上公开内容的工具'
    return_direct = False
    args_schema = SearchArgs

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
