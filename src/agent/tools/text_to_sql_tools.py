import asyncio
from typing import Optional, List
from langchain_core.tools import BaseTool
from pydantic import Field, create_model
from utils.db_utils import MySQLDatabaseManager
from utils.log_utils import log


class ListTablesTool(BaseTool):
    pass
