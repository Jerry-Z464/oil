from datetime import datetime
from flask import Blueprint, request
from application.api.models.alert import Alert
from application.base import Result, DataResult, PageResult
from application.base.AnalysisParam import Param, get_post_data
from application.utils.database import render_sql, file_name
from application.utils.tools import handle_exceptions

monitor_bp = Blueprint('monitor', __name__, url_prefix='/monitor')


@monitor_bp.route('/status', methods=['GET'])
@handle_exceptions(msg="获取设备在线状态失败！")
def get_status():
    data = {
        "data_flow_status": {"status": 'normal', "value": '正常'},
        "database_health": {"status": 'warning', "value": '97.2%'},
        "transmitter_status": {"status": 'normal', "value": '正常'},
        "current_alerts": {"status": 'error', "value": '3个'}
    }
    return DataResult.success(data=data)


@monitor_bp.route('/alerts', methods=['GET'])
@handle_exceptions(msg="获取警告类型失败！")
def get_alerts():
    data = {
        "critical_alerts": 1,
        "warning_alerts": 10,
        "notifications_sent": 6,
        "suppressed_alerts": 3
    }

    return Result.success(data)


@monitor_bp.route('/device', methods=['GET'])
@handle_exceptions(msg="获取数据流失败！")
def get_device():
    params = [
        Param(name='startTime', param_type=str, required=False),
        Param(name='endTime', param_type=str, required=False)
    ]
    current_time = datetime.now().strftime("%H:%M:%S")
    data = [
      {"name": 'device01', "data": [{"time": '09:45', "value": 87.36}, {"time": '09:46', "value": 88.32},
                                    {"time": '09:47', "value": 86.21}, {"time": '09:48', "value": 87.54}]},
      {"name": 'device02', "data": [{"time": '09:45', "value": 84.25}, {"time": '09:46', "value": 84.87},
                                    {"time": '09:47', "value": 85.69}, {"time": '09:48', "value": 87.25}]},
      {"name": 'device03', "data": [{"time": '09:45', "value": 89.21}, {"time": '09:46', "value": 88.45},
                                    {"time": '09:47', "value": 88.12}, {"time": '09:48', "value": 87.96}]}
    ]

    return DataResult.success(data=data)


@monitor_bp.route('/database', methods=['GET'])
@handle_exceptions(msg="获取数据库健康状况失败！")
def get_database():
    data = [
      {"name": '正常数据', "data": 1430},
      {"name": '重复数据', "data": 5},
      {"name": '缺失数据', "data": 5}
    ]
    return DataResult.success(data=data)


@monitor_bp.route('/temperature', methods=['GET'])
@handle_exceptions(msg="获取温度数据失败！")
def get_temperature():
    params = [
        Param(name='startTime', param_type=str, required=False),
        Param(name='endTime', param_type=str, required=False)
    ]
    query = get_post_data(request, params)
    data = [
        {"name": "device01", "data": [{"time": '09:45', "value": 23.51},
            {"time": '09:46', "value": 22.69},
            {"time": '09:47', "value": 23.51},
            {"time": '09:48', "value": 21.69},
            {"time": '09:49', "value": 20.69},
            {"time": '09:50', "value": 23.69},
            ]},
        {"name": "device02", "data": [{"time": '09:45', "value": 13.51},
                                      {"time": '09:46', "value": 12.69},
                                      {"time": '09:47', "value": 13.51},
                                      {"time": '09:48', "value": 11.69},
                                      {"time": '09:49', "value": 10.69},
                                      {"time": '09:50', "value": 13.69},
                                      ]}
    ]
    return DataResult.success(data=data)


@monitor_bp.route('/transmitter', methods=['GET'])
@handle_exceptions(msg="获取温度数据失败！")
def get_transmitter():
    params = [
        Param(name='code', param_type=str, required=True),
        Param(name='startTime', param_type=str, required=False),
        Param(name='endTime', param_type=str, required=False)
    ]
    query = get_post_data(request, params)
    data = [
        {
            "data": [
                {"time": '09:45', "value": 60.36}, {"time": '09:46', "value": 65.21},
                {"time": '09:47', "value": 58.36}, {"time": '09:48', "value": 63.21}
            ],
            "name": "Differential Pressure DP(kPa)",
            "yAxisIndex": 0
        },
        {
            "data": [
                {"time": '09:45', "value": 305.32}, {"time": '09:46', "value": 306.52},
                {"time": '09:47', "value": 307.84}, {"time": '09:48', "value": 910.52}
            ],
            "name": "Pressure(psi)",
            "yAxisIndex": 1
        }
    ]
    return DataResult.success(data=data)


@monitor_bp.route('/alarm_information', methods=['GET'])
@handle_exceptions(msg="获取最新告警信息失败！")
def get_alarm_information():
    params = [
        Param(name='pageNumber', param_type=int, required=True),
        Param(name='pageSize', param_type=int, required=True),
    ]
    query = get_post_data(request, params)
    page_number = query.pageNumber
    page_size = query.pageSize

    query_obj = Alert.query.with_entities(
        Alert.alert_level,
        Alert.suggestion,
        Alert.trigger_time
    )

    pagination = query_obj.paginate(page=page_number, per_page=page_size, error_out=False)

    # 3. 组装返回数据
    data = [{
            "alertType": item[0],
            "alertMsg": item[1],
            "alertTime": item[2].isoformat() if item[2] else None
        } for item in pagination.items]
    return PageResult.success(total=pagination.total, page_number=page_number, page_size=page_size,
                              pages=(pagination.total // query.pageSize) + 1, data=data)
