from collections import namedtuple
from datetime import datetime
from functools import wraps
from application import logger
from application.base import Result

"""
工具类
"""


# 把数据格式转换成指定的格式
def format_datetime(value, formater='%Y-%m-%d %H:%M:%S'):
    """如果值是 datetime 对象，则格式化为字符串；否则返回原值"""
    if isinstance(value, datetime):
        return value.strftime(formater)
    return value


# 获取sql返回的所有字段
def get_all_columns(data_list):
    # 获取列名
    columns = [col for col in data_list.keys()]
    rows = data_list.fetchall()
    return [
        {col: format_datetime(value) for col, value in zip(columns, row)}
        for row in rows
    ]


# 获取传参(不为空）
def get_query_columns(data, *keys):
    for key in keys:
        if key not in data or data[key] is None or data[key] == '':
            raise ValueError("invalid parameter " + key)

    QueryResult = namedtuple('QueryResult', ' '.join(keys))
    result = QueryResult(**{key: data.get(key) for key in keys})
    return result


# 获取字段并返回
def verification_none(*keys):
    for key in keys:
        print(key)
        if not key:
            raise ValueError("invalid parameter " + key)


# 异常捕获
def handle_exceptions(func=None, **deco_kwargs):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ValueError as e:
                return Result.failed(msg=str(e))
            except Exception as e:
                logger.exception(e)
                return Result.failed(msg=deco_kwargs.get('msg', '系统异常'))
        return wrapper
    if func is None:
        return decorator
    else:
        return decorator(func)

