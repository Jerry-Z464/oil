from flask import Blueprint, request
from sqlalchemy import text
from application import db
from application.base import Result, DataResult, PageResult
from application.base.AnalysisParam import Param, get_post_data
from application.entity import Alarm
from application.utils.database import render_sql, file_name
from application.utils.tools import handle_exceptions

alarm_bp = Blueprint('alarm', __name__, url_prefix='/alarm')


@alarm_bp.route('/list', methods=['GET'])
@handle_exceptions(msg="获取告警列表失败！")
def get_alarm_list():
    params = [
        Param(name='startTime', param_type=str, required=False),
        Param(name='endTime', param_type=str, required=False),
        Param(name='pageNumber', param_type=int, required=True),
        Param(name='pageSize', param_type=int, required=True)
    ]
    query = get_post_data(request, params)
    alarm_list = render_sql(file_name('alarm_list'), {
        "startTime": query.startTime,
        "endTime": query.endTime,
        'confined': (query.pageNumber - 1) * query.pageSize,
        'offset': query.pageSize
    })
    results = db.session.execute(alarm_list).fetchall()
    # 将结果转换为 JSON 格式并返回
    items_json = [{
            "id": item.id,
            "code": item.code,
            "alarmType": item.alarm_type,
            "level": item.level,
            "metric": item.metric,
            "currentValue": item.current_value,
            "threshold": item.threshold,
            "suggestion": item.suggestion,
            "alarmTime": item.alarm_time.strftime('%Y-%m-%d %H:%M:%S'),
            "status": item.status
        } for item in results]
    # 执行总数查询
    total_result = db.session.execute(text("SELECT FOUND_ROWS() AS total"))
    total = total_result.fetchone()[0]
    return PageResult.success(total=total, page_number=query.pageNumber, page_size=query.pageSize,
                              pages=(total // query.pageSize) + 1, data=items_json)


@alarm_bp.route('/byId', methods=['GET'])
@handle_exceptions(msg="获取告警详细内容失败！")
def get_alarm_by_id():
    params = [
        Param(name='id', param_type=int, required=True),
    ]
    query = get_post_data(request, params)
    alarm = Alarm.query.get(query.id)
    data = alarm.to_dict()
    return DataResult.success(data=data)


@alarm_bp.route('/delete', methods=['POST'])
@handle_exceptions(msg="删除告警内容失败！")
def alarm_delete():
    params = [
        Param(name='id', param_type=int, required=True),
    ]
    query = get_post_data(request, params)
    alarm = Alarm.query.get(query.id)
    if not alarm:
        return Result.failed(msg="告警不存在")
    alarm.valid = 0
    db.session.commit()
    return Result.success(msg="删除告警成功")

