import asyncio
from typing import Optional, List

from langchain_core.tools import BaseTool
from pydantic import Field, create_model

from agent.utils.db_utils import MySQLDatabaseManager
from agent.utils.log_utils import log


class ListTablesTool(BaseTool):
    """列出数据库中的所有表及其描述信息"""
    name: str = "sql_db_list_tables"
    description: str = "列出MySQL数据库中的所有表名及其描述信息。"
    db_manager: MySQLDatabaseManager

    def _run(self) -> str:
        try:
            tables_info = self.db_manager.get_tables_with_comments()
            result = f"数据库总共有{len(tables_info)}个表：\n\n"
            for i, table_info in enumerate(tables_info):
                table_name = table_info['table_name']
                table_comment = table_info['table_comment']
                description_display = table_comment if table_comment and not table_comment.isspace() else "(暂无描述)"
                result += f"{i + 1}. 表名：{table_name}\n 描述：{description_display}\n\n"
            log.error(result)
            return result
        except Exception as e:
            log.exception(e)
            return f'列出表时出错:{str(e)}'

    async def _arun(self) -> str:
        return await asyncio.to_thread(self._run)


class TableSchemaTool(BaseTool):
    '''获取表模式信息'''
    name: str = 'sql_db_schema'
    description: str = '获取表结构'
    db_manager: MySQLDatabaseManager

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args_schema = create_model(
            "TableSchemaToolArgs",
            # table_names=(Optional[List[str]], Field(..., description='表名列表')),
            table_names=(
            Optional[List[str]], Field(..., description='用逗号分隔的表名列表，例如：t_usermodel,t_rolemodel'))

        )

    def _run(self, table_names: Optional[List[str]] = None) -> str:
        try:
            schema_info = self.db_manager.get_table_schema(table_names)
            return schema_info if schema_info else "未找到匹配的表。"
        except Exception as e:
            log.exception(e)
            return f"返回表结构时出错：{str(e)}"

    async def _arun(self, table_names: Optional[List[str]] = None) -> str:
        return await asyncio.to_thread(self._run, table_names)


class SQLQueryTool(BaseTool):
    """执行SQL查询"""
    name: str = 'sql_db_query'
    description: str = "在MySQL数据库上执行安全的SELECT查询并返回结果。"
    db_manager: MySQLDatabaseManager

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args_schema = create_model(
            "SQLQueryToolArgs",
            query=(str, Field(..., description="有效的SQL查询语句"))
        )

    # 同步兼容
    def _run(self, query: str) -> str:
        try:
            result = self.db_manager.execute_sql(query)
            log.error(f"{query}--11111111111111--{result}")

            return str(result)
        except Exception as e:
            log.exception(e)
            return f'执行查询时出错:{str(e)}'

    async def _arun(self, query: str) -> str:
        try:
            result = await asyncio.to_thread(self.db_manager.execute_sql, query)
            return str(result)
        except Exception as e:
            log.exception(e)
            return f"执行查询时出错：{str(e)}"


class SQLQueryCheckerTool(BaseTool):
    """检查SQL查询语法"""
    name: str = "sql_db_query_checker"
    description: str = "检查SQL语法"
    db_manager: MySQLDatabaseManager

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args_schema = create_model(
            "SQLQueryCheckerToolArgs",
            query=(str, Field(..., description='需要检查的SQL'))
        )

    def _run(self, query: str) -> str:
        try:
            return self.db_manager.preprocess_sql(query)
        except Exception as e:
            log.exception(e)
            return f"执行检查时出错：{str(e)}"

    async def _arun(self, query: str) -> str:
        try:
            return await asyncio.to_thread(self.db_manager.preprocess_sql, query)
        except Exception as e:
            log.exception(e)
            return f"执行检查时出错：{str(e)}"


if __name__ == '__main__':
    # 配置数据库连接信息
    host = "localhost"
    port = 3306
    username = "root"
    password = "123456"
    database = "nl_to_sql_db"
    connection_string = f"mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8"
    manager = MySQLDatabaseManager(connection_string)

    # 测试工具
    tool = ListTablesTool(db_manager=manager)
    print(tool.invoke({}))

    tool = TableSchemaTool(db_manager=manager)
    print(tool.invoke({"table_names": ['student_info']}))
    #
    tool = SQLQueryCheckerTool(db_manager=manager)
    print(tool.invoke({"query": "SELECT count(1) FROM student_info"}))
    #
    tool = SQLQueryTool(db_manager=manager)
    print(tool.invoke({"query": "SELECT id FROM student_info"}))
