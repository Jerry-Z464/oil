from flask import jsonify


def __init__(self, code, msg=None, data=None):
    self.code = code
    if msg is None:
        msg = ""
    self.msg = msg
    if data is None:
        data = []
    self.data = data


def success(msg="成功", data=None):
    # 定义可自动转换的类型
    auto_convertible_types = (dict, list, str, int, float, bool, type(None))

    # 如果 data 是非 None 且不可直接序列化，尝试自动转换
    if data is not None and not isinstance(data, auto_convertible_types):
        try:
            # 尝试转换为字典（适用于简单对象）
            data = data.to_dict() if hasattr(data, 'to_dict') else vars(data)
        except Exception as e:
            # 转换失败时返回错误信息
            return jsonify(code=400, msg=f"数据转换失败: {str(e)}", data=None)

    try:
        # 尝试生成 JSON 响应
        return jsonify(code=200, msg=msg, data=data)
    except Exception as e:
        # 捕获 JSON 序列化异常
        return jsonify(code=500, msg=f"服务器内部错误: {str(e)}", data=None)

