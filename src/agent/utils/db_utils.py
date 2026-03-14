from typing import List, Optional, Dict, Any

from dns.e164 import query
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

from agent.utils.log_utils import log


class MySQLDatabaseManager:
    ''' Mysql 数据库甘利奇，负责数据库连接和基本操作'''

    def __init__(self, connection_string: str):
        '''
        初始化MySQL
        :param connection_string:
        '''
        self.engine = create_engine(connection_string,
                                    pool_size=5,
                                    pool_recycle=3600
                                    )

    def get_table_names(self) -> list[str]:
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            log.exception(e)
            raise ValueError(f'获取表名失败:{str(e)}')

    def get_tables_with_comments(self) -> List[dict]:
        '''
        获取数据库中所有表的名称和描述信息
        Returns:
            List[dict]: 一个字典列表，每个字典
        :return:
        '''
        try:
            query = text('''
            SELECT TABLE_NAME, TABLE_COMMENT
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                  AND TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_NAME 
            ''')
            with self.engine.connect() as connection:
                result = connection.execute(query)
                return [
                    {"table_name": row[0], "table_comment": row[1]}
                    for row in result
                ]
        except SQLAlchemyError as e:
            log.exception(e)
            raise ValueError(f"获取表名及描述信息失败：{str(e)}")

    def get_table_schema(self, table_names: Optional[List[str]] = None) -> str:
        '''
               获取指定表的模式信息（包含字段注释/主键/外键/索引）
        Args:
            table_names: 表名列表，为空则获取所有表
        '''
        try:
            inspector = inspect(self.engine)
            schema_info: List[str] = []
            tables_to_process = table_names if table_names else self.get_table_names()
            for table_name in tables_to_process:
                columns = inspector.get_columns(table_name)
                pk_constraint = inspector.get_pk_constraint(table_name)
                primary_keys = pk_constraint.get('constrained_columns', []) if pk_constraint else []
                foreign_keys = inspector.get_foreign_keys(table_name)
                indexs = inspector.get_indexes(table_name)

                table_schema = f'表名:{table_name}\n 列信息:\n'
                for col in columns:
                    pk_indicator = "(主键)" if col["name"] in primary_keys else ""
                    comment = col.get("comment", "无注释")
                    table_schema += f" - {col['name']} : {col['type']} {pk_indicator} [注释: {comment}]\n"
                if foreign_keys:
                    table_schema += "外键信息:\n"
                    for fk in foreign_keys:
                        table_schema += f" - 列 {fk['constrained_columns']} -> {fk['referred_table']}({fk['referred_columns']})\n"
                if indexs:
                    table_schema += "索引信息:\n"
                    for idx in indexs:
                        table_schema += f" - {idx['name']} : {idx['column_names']} 唯一: {idx.get('unique', False)}\n"
                table_schema += "\n"
                schema_info.append(table_schema)
            return "\n".join(schema_info)
        except Exception as e:
            log.exception(e)
            raise ValueError(f"获取表结构失败:{str(e)}")

    # =========================
    # SQL 预处理
    # =========================
    def preprocess_sql(self, sql: str) -> str:
        try:
            if not sql:
                raise ValueError("SQL 不能为空")
            sql = sql.strip().rstrip(";")
            lower_sql = sql.lower()
            if not lower_sql.startswith("select"):
                raise ValueError("仅允许执行 SELECT 查询")
            forbidden = [
                " drop ",
                " truncate ",
                " delete ",
                " update ",
                " insert ",
                " alter ",
                " create ",
                " grant ",
                " revoke ",
            ]
            for keyword in forbidden:
                if keyword in lower_sql:
                    raise ValueError(f'检测到危险sql操作：{keyword.strip()}')
            # 语法教育
            explain_sql = f"EXPLAIN {sql}"
            with self.engine.connect() as connection:
                connection.execute(text(explain_sql))
            return sql  # 返回原SQL
        except SQLAlchemyError as e:
            raise ValueError(f"SQL 语法或表结构错误: {str(e)}")
        except Exception as e:
            log.exception(e)
            raise

    # =========================
    # SQL 执行
    # =========================
    def execute_sql(
            self,
            sql: str,
            params: Optional[Dict[str, Any]] = None,
            limit: Optional[int] = 100,
    ) -> List[Dict[str, Any]]:
        try:
            safe_sql = self.preprocess_sql(sql)

            # 自动加 limit
            if limit and " limit " not in safe_sql.lower():
                safe_sql = f"{safe_sql} LIMIT {limit}"

            with self.engine.connect() as connection:
                result = connection.execute(text(safe_sql), params or {})
                columns = result.keys()
                rows = result.fetchmany(100)
                if not rows:
                    return "查询结果为空"

                return [dict(zip(columns, row)) for row in result]

        except SQLAlchemyError as e:
            log.exception(e)
            raise ValueError(f"SQL 执行失败: {str(e)}")

    def validate_query(self, query: str) -> str:
        '''
        验证 sql 查询语法是否正确
        Args:
            query:要验证的SQL查询
        '''
        # 基本语法检查
        if not query or not query.strip():
            return "错误:插叙不能为空"
        # 检查是否以SELECT 或with 开头
        query_lower = query.lower().strip()
        if not query_lower.startswith(('select', 'with')):
            return '警告:建议使用SELECT或WITH 查询，其他操作可能被限制'
        # 插叙解析查询(不实际执行)
        try:
            with self.engine.connect() as connection:
                # 使用SQLAlchemy的text()来解析但不执行
                parsed_query = text(query)
                # 尝试编译查询来检查语法
                compiled = parsed_query.compile(compile_kwargs={"literal_binds": True})
                return 'SQL查询语法看起来正确'
        except Exception as e:
            pass


if __name__ == '__main__':
    host = "localhost"
    port = 3306
    username = "root"
    password = "123456"
    database = "nl_to_sql_db"
    connection_string = f"mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8"
    manager = MySQLDatabaseManager(connection_string)

    # 测试表名及描述
    tables_info = manager.get_tables_with_comments()
    print(tables_info)

    # 测试表结构
    schema = manager.get_table_schema(['student_info'])
    print(schema)

    # 测试SQL预处理
    sql_safe = manager.preprocess_sql("SELECT id FROM student_info")
    print(sql_safe)

    # 测试SQL执行
    result = manager.execute_sql("SELECT id FROM student_info")
    print(result)
