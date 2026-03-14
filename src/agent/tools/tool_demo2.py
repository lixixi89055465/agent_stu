from typing import Any

from dns.e164 import query
from langchain_core.tools import BaseTool

from agent.my_llm import zhipuai_client


class MyWebSearchTool(BaseTool):
    def _run(self, query: str) -> Any:
        try:
            response = zhipuai_client.web_search(
                search_engine='search_pro',
                search_query=query
            )
            if response.search_result:
                return '\n\n'.join([d.content for d in response.search_result])
            return "没有搜索到任务内容"
        except Exception as e:
            print(e)
            return "没有搜索到任务内容"

    async def _run(self, query: str) -> str:
        return self._run(query)
