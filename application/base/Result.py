from flask import jsonify


def __init__(self, code, msg=None):
    self.code = code
    self.msg = msg


def success(data=None, msg="成功"):
    result = {"code": 200, "msg": msg}
    if data is not None:
        result["data"] = data
    return jsonify(result)


def failed(msg="失败"):
    return jsonify(code=400, msg=msg)
