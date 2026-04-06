from typing import Annotated

from langchain_core.tools import tool
from pydantic import Field, BaseModel


@tool('calculate')
def calculate3(
        a: Annotated[float, '第一个需要输入的数字'],
        b: Annotated[float, '第二个需要输入的数字'],
        operation: Annotated[str, '运算类型，只能是add,subtract,multiply和divide中的任意一个']) -> float:
    '''工具函数：计算两个数字的运算结果'''
    print(f'调用 calculate 工具，第一个数字：{a},'
          f'第二个数据:{b},运算类型:{operation}')
    result = 0.0
    match operation:
        case 'add':
            result = a + b
        case 'subtract':
            result = a - b
        case 'multiply':
            result = a * b
        case 'divide':
            if b != 0:
                result = a / b
            else:
                raise ValueError('除数不能为零')
    return result


print(calculate3.name)
print(calculate3.description)
print(calculate3.args)
print(calculate3.args_schema.model_json_schema())
print(calculate3.return_direct)
print(calculate3.invoke({'a': 40, 'b': 2, 'operation': 'add'}))
