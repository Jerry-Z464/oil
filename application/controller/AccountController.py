import time

from flask import Blueprint, request, g
from passlib.handlers.sha2_crypt import sha256_crypt
from sqlalchemy import text

from application import db
from application.base import Result, DataResult, PageResult
from application.base.AnalysisParam import Param, get_post_data
from application.entity import Account, UserToken
from application.utils import EncodeUtils
from application.utils.auth import ignore_security
from application.utils.database import render_sql, file_name
from application.utils.tools import handle_exceptions

account_bp = Blueprint('account', __name__, url_prefix='/account')


# 注册
@account_bp.route('register', methods=['POST'])
@handle_exceptions(msg="注册失败")
def add_account():
    params = [
        Param(name='password', param_type=str, required=True),
        Param(name='name', param_type=str, required=True),
        Param(name='email', param_type=str, required=True),
        Param(name='deptId', param_type=int, required=False),
        Param(name='role', param_type=int, required=True),
        Param(name='phoneNumber', param_type=str, required=True),
        Param(name='profilePhoto', param_type=str, required=False),
        Param(name='remark', param_type=str, required=False)
    ]
    query = get_post_data(request, params)
    # 检查账号是否已存在
    existing_account = Account.query.filter_by(name=query.name).one_or_none()
    if existing_account:
        return Result.failed(msg="该账号已存在！")
    # 检查邮箱是否已存在
    existing_email = Account.query.filter_by(email=query.email).one_or_none()
    if existing_email:
        return Result.failed(msg="该邮箱已存在！")
    account = Account(password=EncodeUtils.generate_sha256(query.password), name=query.name,
                      email=query.email, dept_id=query.deptId, role=query.role, phone_number=query.phoneNumber)
    if query.profilePhoto:
        account.profile_photo = query.profilePhoto
    if query.remark:
        account.remark = query.remark
    db.session.add(account)
    db.session.commit()
    return Result.success()


# 登录
@ignore_security
@account_bp.route('login', methods=['POST'])
@handle_exceptions(msg="登录失败")
def login():
    params = [
        Param(name='username', param_type=str, required=True),
        Param(name='password', param_type=str, required=True)
    ]
    query = get_post_data(request, params)
    account = Account.query.filter_by(name=query.username, valid=1).one_or_none()
    if account is None:
        return Result.failed(msg="用户不存在！")
    # 校验密码
    if sha256_crypt.verify(query.password, account.password):
        # 生成token
        token = EncodeUtils.generate_token(account.id, account.role)
        # token 存入数据库 1.查询是否存在，存在则更新，不存在则插入
        exit_token = UserToken.query.filter_by(user_id=account.id).one_or_none()
        timestamp = int(time.time())
        if exit_token:
            exit_token.timestamp = timestamp
            exit_token.token = token
        else:
            user_token = UserToken(user_id=account.id, token=token, timestamp=timestamp)
            db.session.add(user_token)
        db.session.commit()
        item_json = {
            "id": account.id,
            "name": account.name,
            "role": account.role,
            "token": token
        }
        return DataResult.success(data=item_json)
    return Result.failed(msg="账号或密码错误！")


# 修改密码
@account_bp.route('change_password', methods=['POST'])
@handle_exceptions(msg="修改密码失败")
def change_password():
    params = [
        Param(name='oldPassword', param_type=str, required=True),
        Param(name='newPassword', param_type=str, required=True)
    ]
    query = get_post_data(request, params)
    account = Account.query.filter_by(id=g.user_id, valid=1).one_or_none()
    if account is None:
        return Result.failed(msg="用户不存在！")
    if sha256_crypt.verify(query.oldPassword, account.password):
        return Result.failed(msg="旧密码错误！")
    if query.newPassword == query.newPassword:
        return Result.failed(msg="新旧密码不能相同！")
    account.password = EncodeUtils.generate_sha256(query.newPassword)
    db.session.commit()
    return Result.success()


# 重置密码
@account_bp.route('reset_password', methods=['POST'])
@handle_exceptions(msg="重置密码失败")
def reset_password():
    params = [
        Param(name='resetAccountId', param_type=int, required=True),
        Param(name='resetPassword', param_type=str, required=True)
    ]
    query = get_post_data(request, params)
    account = Account.query.filter_by(id=query.resetAccountId, valid=1).one_or_none()
    if account is None:
        return Result.failed(msg="用户不存在！")
    account.password = EncodeUtils.generate_sha256(query.resetPassword)
    db.session.commit()
    return Result.success()


# 登出
@account_bp.route('logout', methods=['POST'])
@handle_exceptions
def logout():
    pass


# 获取个人信息
@account_bp.route('info', methods=['GET'])
@handle_exceptions
def get_info():
    account = Account.query.filter_by(id=g.user_id, valid=1).one_or_none()
    if account is None:
        return Result.failed(msg="用户不存在！")
    item_json = {
        'id': account.id,
        'account': account.account,
        'name': account.name,
        'email': account.email,
        'deptId': account.dept_id,
        'role': account.role,
        'phoneNumber': account.phone_number,
        'profilePhoto': account.profile_photo,
        'work': account.work
    }
    return DataResult.success(data=item_json)


# 用户列表查询
@account_bp.route('list', methods=['GET'])
@handle_exceptions
def get_all_user_list():
    params = [
        Param(name='name', param_type=str, required=False),
        Param(name='deptId', param_type=int, required=False),
        Param(name='role', param_type=int, required=False),
        Param(name='phoneNumber', param_type=str, required=False),
        Param(name='email', param_type=str, required=False),
        Param(name='pageNumber', param_type=int, required=True, default=1),
        Param(name='pageSize', param_type=int, required=True, default=10)
    ]
    query = get_post_data(request, params)
    user_list = render_sql(file_name('user_list'), {
        'name': query.name,
        'email': query.email,
        'phoneNumber': query.phoneNumber,
        'role': query.role,
        'deptId': query.deptId,
        'confined': (query.pageNumber - 1) * query.pageSize,
        'offset': query.pageSize
    })
    results = db.session.execute(user_list).fetchall()
    # 将结果转换为 JSON 格式并返回
    items_json = [{'id': item.id,
                   'name': item.name,
                   'email': item.email,
                   'phoneNumber': item.phoneNumber,
                   'role': item.role,
                   'work': item.work,
                   'deptId': item.deptId,
                   'deptName': item.deptName} for item in results]
    # 执行总数查询
    total_result = db.session.execute(text("SELECT FOUND_ROWS() AS total"))
    total = total_result.fetchone()[0]
    return PageResult.success(total=total, page_number=query.pageNumber, page_size=query.pageSize,
                              pages=(total // query.pageSize) + 1, data=items_json)

