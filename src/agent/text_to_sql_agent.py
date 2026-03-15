from typing import List
from langchain.agents import create_agent
from langchain_core.tools import BaseTool
from sqlalchemy.testing import db

from agent.my_llm import llm
from agent.tools.text_to_sql_tools import ListTablesTool, TableSchemaTool, SQLQueryCheckerTool, SQLQueryTool
from agent.utils.db_utils import MySQLDatabaseManager


def get_tools(host: str, port: int, username: str, password: str, database: str) -> List[BaseTool]:
    # 构建连接字符串
    connection_string = f"mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8"
    manager = MySQLDatabaseManager(connection_string)
    return [
        ListTablesTool(db_manager=manager),
        TableSchemaTool(db_manager=manager),
        SQLQueryCheckerTool(db_manager=manager),
        SQLQueryTool(db_manager=manager),
    ]


# 配置数据库连接信息
host = "localhost"
port = 3306
username = "root"
password = "123456"
database = "nl_to_sql_db"

tools = get_tools(host, port, username, password, database)
system_prompt = """
    你是一个专门用于与 SQL 数据库交互的 AI 智能体，负责将自然语言问题转换为安全、准确的 SQL 查询并返回结果。
    你必须严格遵循以下工作流程：
    先查看数据库中可用的表及其结构信息。
    根据用户问题生成符合 {dialect} 语法的 SQL 查询语句。
    查询语句仅可使用只读 SELECT 操作。
    除非用户明确指定数量，否则结果最多返回 {top_k} 条。
    仅选择必要字段，禁止使用 SELECT *。
    可通过排序提升结果相关性。
    在执行前必须检查 SQL 语法与安全性。
    若执行失败，需自动修正 SQL 并重试。
    基于最终查询结果生成答案，而非凭空推测。
    """.format(
    dialect="MySQL",
    # dialect=db.dialect,
    top_k=5
)
agent = create_agent(
    llm,
    tools=tools,
    system_prompt=system_prompt
)

if __name__ == '__main__':
    for step in agent.stream(
            input={
                "messages": [{"role": "user", "content": "数据库中有多少个部门，每个部门都有哪些员工?"}]},
            stream_mode="values"
    ):
        step['messages'][-1].pretty_print()  # 打印
