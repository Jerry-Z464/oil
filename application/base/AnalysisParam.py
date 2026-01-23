import ast
from collections import namedtuple
from application.utils import CheckUtils


class Param:
    """
    目前仅支持int和str
    name: 参数名称
    param_type: 参数类型
    required: 是否必填
    default: 默认值
    """
    def __init__(self, name, param_type, required=False, default=None):
        self.name = name
        self.type = param_type
        self.required = required
        self.default = default

        # 支持的类型转换函数映射
        self.type_converters = {
            int: convert_to_int,
            str: convert_to_str,
            bool: convert_to_bool
        }


def get_post_data(req, params):
    if req.method in ('GET', 'DELETE'):
        # GET 和 DELETE 请求通常使用查询参数
        data = req.args
    elif req.method in ('POST', 'PUT'):
        if req.content_type:
            if req.content_type.startswith('application/json'):
                # JSON 格式数据
                try:
                    data = req.get_json()
                except Exception as e:
                    raise ValueError(f"Invalid JSON data: {str(e)}")
            elif req.content_type.startswith('multipart/form-data') or req.content_type.startswith(
                    'application/x-www-form-urlencoded'):
                # 表单数据
                data = req.form
            else:
                # 不支持的 Content-Type
                raise ValueError(f"Unsupported Content-Type: {req.content_type} for {req.method} method")
        else:
            # 如果没有提供 Content-Type，默认尝试解析为表单数据
            data = req.form
    else:
        # 不支持的 HTTP 方法
        raise ValueError(f"Unsupported HTTP method: {req.method}")
    result = {}

    # 参数校验
    for param in params:
        # 获取参数值
        value = data.get(param.name)

        # 如果是必填参数且没有值，返回失败
        if param.required and value is None:
            raise ValueError(f"Parameter '{param.name}' is required.")

        # 如果有默认值且没有提供，使用默认值
        if value is None and param.default is not None:
            value = param.default

        try:
            # 类型校验和重组
            result[param.name] = param.type_converters[param.type](value, param.required)
        except (ValueError, TypeError):
            raise ValueError(f"Parameter '{param.name}' must be of type {param.type.__name__}.")

    QueryResult = namedtuple('QueryResult', ' '.join(result.keys()))
    return QueryResult(**{key: result.get(key) for key in result.keys()})


def convert_to_int(value, required):
    if not required and CheckUtils.is_blank(value):
        return None
    return int(value)


def convert_to_str(value, required):
    if not required and CheckUtils.is_blank(value):
        return None
    return str(value)


def convert_to_bool(value, required):
    if not required and CheckUtils.is_blank(value):
        return None
    if type(value) is not bool:
        value = value[0].upper() + value[1:]
        return ast.literal_eval(value)
    else:
        return value
