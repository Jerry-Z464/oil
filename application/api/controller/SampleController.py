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


# @sample_bp.route("del", methods=['POST'])
# @handle_exceptions
# def add_dept():
#     params = [
#         Param(name='sample', param_type=str, required=True),
#         Param(name='startTime', param_type=str, required=True),
#         Param(name='endTime', param_type=str, required=True)
#     ]
#     query = get_post_data(request, params)
#     points = query.sample.split(',')
#     for point in points:
#         try:
#             Decimal(point)
#         except Exception as e:
#             return Result.failed("无效的采样点")
#     sample = WaterCutSample(query.sample, query.startTime, query.endTime)
#     db.session.add(sample)
#     db.session.commit()
#     return Result.success()
#
#
# @sample_bp.route("add", methods=['POST'])
# @handle_exceptions
# def add_dept():
#     params = [
#         Param(name='sample', param_type=str, required=True),
#         Param(name='startTime', param_type=str, required=True),
#         Param(name='endTime', param_type=str, required=True)
#     ]
#     query = get_post_data(request, params)
#     points = query.sample.split(',')
#     for point in points:
#         try:
#             Decimal(point)
#         except Exception as e:
#             return Result.failed("无效的采样点")
#     sample = WaterCutSample(query.sample, query.startTime, query.endTime)
#     db.session.add(sample)
#     db.session.commit()
#     return Result.success()
