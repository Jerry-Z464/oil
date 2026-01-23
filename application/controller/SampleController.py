from flask import Blueprint, request
from decimal import Decimal
from application import db
from application.base import Result, DataResult
from application.base.AnalysisParam import Param, get_post_data
from application.entity import WaterCutSample
from application.utils.database import render_sql, file_name
from application.utils.tools import handle_exceptions

sample_bp = Blueprint('sample', __name__, url_prefix='/sample')


@sample_bp.route("add", methods=['POST'])
@handle_exceptions
def add_dept():
    params = [
        Param(name='sample', param_type=str, required=True),
        Param(name='startTime', param_type=str, required=True),
        Param(name='endTime', param_type=str, required=True)
    ]
    query = get_post_data(request, params)
    points = query.sample.split(',')
    for point in points:
        try:
            Decimal(point)
        except Exception as e:
            return Result.failed("无效的采样点")
    sample = WaterCutSample(query.sample, query.startTime, query.endTime)
    db.session.add(sample)
    db.session.commit()
    return Result.success()


# @dept_bp.route("", methods=['PUT'])
# @handle_exceptions(msg="修改部门失败！")
# def update_dept():
#     params = [
#         Param(name='id', param_type=int, required=True),
#         Param(name='name', param_type=str, required=False)
#     ]
#     query = get_post_data(request, params)
#     dept = Dept.query.get(query.id)
#     if dept is None:
#         return Result.failed("无效部门id")
#     if query.name is not None:
#         # 查询部门是否存在
#         exit_dept = Dept.query.filter_by(name=query.name, parent_id=dept.parent_id, valid=1).one_or_none()
#         if exit_dept is not None and exit_dept.id != query.id:
#             return Result.failed(msg="部门已存在！")
#         dept.name = query.name
#         db.session.commit()
#     return Result.success()
#
#
# @dept_bp.route("", methods=['GET'])
# @handle_exceptions(msg="获取部门列表失败！")
# def get_dept():
#     content = render_sql(file_name('dept_list'))
#     results = db.session.execute(content).fetchall()
#     data = parse_dept_tree(results)
#     return DataResult.success(data=data)
#
#
# @dept_bp.route("", methods=['DELETE'])
# @handle_exceptions(msg="删除部门失败！")
# def delete_dept():
#     params = [
#         Param(name='id', param_type=int, required=True)
#     ]
#     query = get_post_data(request, params)
#     dept = Dept.query.get(query.id)
#     if dept is None:
#         return Result.failed("无效部门id")
#     dept.valid = 0
#     db.session.commit()
#     return Result.success()
