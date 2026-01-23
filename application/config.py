from flask import Blueprint, request
from application.api.models.data_fields import DataFields
from application.base import Result, PageResult
from application.base.AnalysisParam import Param, get_post_data
from application.utils.tools import handle_exceptions
from application import db
config_bp = Blueprint('api_config', __name__, url_prefix='/config')


@config_bp.route('/list', methods=['GET'])
@handle_exceptions(msg="获取数据字段列表失败！")
def get_config_list():
    params = [
        Param(name='field_name', param_type=str, required=False),
        Param(name='data_type', param_type=str, required=False),
        Param(name='pageNumber', param_type=int, required=True),
        Param(name='pageSize', param_type=int, required=True),
    ]
    query = get_post_data(request, params)
    field_name = query.field_name
    data_type = query.data_type
    page_number = query.pageNumber
    page_size = query.pageSize

    # 1. 构造查询条件（模糊匹配姓名）
    query_obj = DataFields.query
    if field_name:
        query_obj = query_obj.filter(DataFields.field_name.like(f'%{field_name}%'))
    if data_type:
        query_obj = query_obj.filter(DataFields.data_type.like(f'%{data_type}%'))
    pagination = query_obj.paginate(page=page_number, per_page=page_size, error_out=False)

    # 3. 组装返回数据
    data = [item.to_dict() for item in pagination.items]
    return PageResult.success(total=pagination.total, page_number=page_number, page_size=page_size,
                              pages=(pagination.total // query.pageSize) + 1, data=data)


@config_bp.route('/field/switch', methods=['POST'])
@handle_exceptions(msg="修改数据字段开关失败！")
def field_switch():
    params = [
        Param(name='id', param_type=int, required=True),
        Param(name='status', param_type=int, required=True),
    ]
    query = get_post_data(request, params)
    field_id = query.id

    data_fields = DataFields.query.get_or_404(field_id)

    data_fields.status = query.status
    db.session.commit()

    return Result.success(msg="修改数据字段开关成功")

@config_bp.route('/field/update', methods=['POST'])
@handle_exceptions(msg="修改数据字段失败！")
def field_update():
    params = [
        Param(name='id', param_type=int, required=True),
        Param(name='unit', param_type=str, required=True),
        Param(name='default_value', param_type=str, required=True),
    ]
    query = get_post_data(request, params)
    field_id = query.id

    data_fields = DataFields.query.get_or_404(field_id)

    data_fields.unit = query.unit
    data_fields.default_value = query.default_value
    db.session.commit()

    return Result.success(msg="修改数据字段成功")

@config_bp.route('/field/delete', methods=['POST'])
@handle_exceptions(msg="删除数据字段失败！")
def field_delete():
    params = [
        Param(name='id', param_type=int, required=True),
    ]
    query = get_post_data(request, params)
    field_id = query.id

    # 1. 根据ID查询员工
    data_fields = DataFields.query.get_or_404(field_id)

    # 2. 删除并提交
    db.session.delete(data_fields)
    db.session.commit()

    return Result.success(msg="删除数据字段成功")