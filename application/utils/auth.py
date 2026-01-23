import time
from application import app, db
from application.entity import UserToken
from application.utils import EncodeUtils
from flask import request, g, jsonify


# 请求前钩子，用于认证
@app.before_request
def authenticate():
    if request.path.startswith('/monitor'):
        return
    view_func = app.view_functions.get(request.endpoint)
    if view_func and hasattr(view_func, 'no_auth_required'):
        return
    if not check_token():
        return jsonify({'code': 401, 'msg': '身份认证失败,请重新登录'})


# 自定义认证函数，您可以根据自己的需求进行修改
def check_token():
    token = request.headers.get('token')
    if token:
        s = token.split(".")
        if len(s) == 3:
            user_id = EncodeUtils.base64_decode(s[0])
            effective_timestamp = int(time.time()) - (app.config["TOKEN_TIME"] * 3600)
            cache_token = UserToken.query.filter(
                UserToken.user_id == user_id,
                UserToken.timestamp >= effective_timestamp).one_or_none()
            if cache_token is not None:
                if token == cache_token.token:
                    # 信息存入上下文
                    g.user_id = int(user_id)
                    g.role = int(s[1])
                    # 刷新token有效期
                    timestamp = int(time.time())
                    cache_token.timestamp = timestamp
                    db.session.commit()
                    db.session.close()
                    return True
    return False


# 装饰器，用于标记不需要认证的路由
def ignore_security(route_func):
    route_func.no_auth_required = True
    return route_func
