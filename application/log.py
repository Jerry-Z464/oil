from flask import Blueprint, request
from application.api.models.log import Log
from application.base import Result, PageResult
from application.base.AnalysisParam import Param, get_post_data
from application.utils.tools import handle_exceptions
from application import db

log_bp = Blueprint('log', __name__, url_prefix='/log')

@log_bp.route('/device', methods=['GET'])
@handle_exceptions(msg="获取设备日志失败！")
def get_device_log():
    params = [
        Param(name='pageNumber', param_type=int, required=True),
        Param(name='pageSize', param_type=int, required=True),
        Param(name='log_content', param_type=str, required=False),
    ]
    query = get_post_data(request, params)
    log_content = query.log_content
    page_number = query.pageNumber
    page_size = query.pageSize

    query_obj = Log.query
    if log_content:
        query_obj = query_obj.filter(Log.log_content.like(f'%{log_content}%'))


    pagination = query_obj.paginate(page=page_number, per_page=page_size, error_out=False)

    # 3. 组装返回数据
    data = [item.to_dict() for item in pagination.items]
    return PageResult.success(total=pagination.total, page_number=page_number, page_size=page_size,
                              pages=(pagination.total // query.pageSize) + 1, data=data)

