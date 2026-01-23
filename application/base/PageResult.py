from flask import jsonify


def __init__(self, code, msg=None, total=0, page_number=0, page_size=0, pages=0, data=None):
    self.code = code
    if msg is None:
        msg = ""
    self.msg = msg
    if data is None:
        data = []
    self.data = data
    self.total = total
    self.pageNumber = page_number
    self.pageSize = page_size
    self.pages = pages


def success(msg="成功", total=0, page_number=0, page_size=0, pages=0, data=None):
    # 定义可自动转换的类型
    auto_convertible_types = (dict, list, str, int, float, bool, type(None))

    # 参数类型检查与转换
    def validate_and_convert(value, param_name, expected_type, default):
        try:
            # 尝试自动转换类型
            if not isinstance(value, expected_type):
                return expected_type(value)
            return value
        except (ValueError, TypeError) as e:
            # 类型转换失败时返回错误信息
            return jsonify(
                code=400,
                msg=f"参数错误: {param_name} 必须是 {expected_type.__name__} 类型",
                data=None
            )

    # 验证分页参数（要求必须是整数）
    total = validate_and_convert(total, "total", int, 0)
    page_number = validate_and_convert(page_number, "page_number", int, 0)
    page_size = validate_and_convert(page_size, "page_size", int, 0)
    pages = validate_and_convert(pages, "pages", int, 0)

    # 检查 data 参数
    if data is not None and not isinstance(data, auto_convertible_types):
        try:
            # 尝试转换为字典（适用于简单对象）
            data = data.to_dict() if hasattr(data, 'to_dict') else vars(data)
        except Exception as e:
            # 转换失败时返回错误信息
            return jsonify(code=400, msg=f"数据转换失败: {str(e)}", data=None)

    try:
        # 尝试生成 JSON 响应
        return jsonify(
            code=200,
            msg=msg,
            total=total,
            pageNumber=page_number,
            pageSize=page_size,
            pages=pages,
            data=data
        )
    except Exception as e:
        # 捕获 JSON 序列化异常
        return jsonify(code=500, msg=f"服务器内部错误: {str(e)}", data=None)
