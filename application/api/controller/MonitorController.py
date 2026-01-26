from flask import Blueprint, request
from application import db
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
        Param(name='code', param_type=str, required=True),
        Param(name='startTime', param_type=str, required=False),
        Param(name='endTime', param_type=str, required=False)
    ]

    data_list = render_sql(file_name('water_cut'))
    results = db.session.execute(data_list).fetchall()

    # 按照指定格式组织数据
    data = [
        {
            "data": [],
            "name": "gas flow rate(m³)"
        },
        {
            "data": [],
            "name": "liquid flow rate(m³)"
        },
        {
            "data": [],
            "name": "oil flow rate(m³)"
        },
        {
            "data": [],
            "name": "water flow rate(m³)"
        }
    ]

    # 将查询结果填充到数据结构中
    for row in results:
        gas_value = round(float(row.gas_flow_rate), 2)
        liquid_value = round(float(row.liquid_flow_rate), 2)
        oil_value = round(float(row.oil_flow_rate), 2)
        water_value = round(float(row.water_flow_rate), 2)
        time_value = row.createTime.strftime("%Y-%m-%d %H:%M:%S")
        data[0]["data"].append({
            "time": time_value,
            "value": gas_value
        })
        data[1]["data"].append({
            "time": time_value,
            "value": liquid_value
        })
        data[2]["data"].append({
            "time": time_value,
            "value": oil_value
        })
        data[3]["data"].append({
            "time": time_value,
            "value": water_value
        })

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
        Param(name='code', param_type=str, required=False),
        Param(name='startTime', param_type=str, required=False),
        Param(name='endTime', param_type=str, required=False)
    ]
    data_list = render_sql(file_name('temperature_list'))
    results = db.session.execute(data_list).fetchall()

    # 按照指定格式组织数据
    data = {
            "data": [{'time': item.createTime.strftime("%Y-%m-%d %H:%M:%S"),
                      'value': round(float(item.temperature), 2)} for item in results],
            "name": "temperature(℃)"
        }
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

    data_list = render_sql(file_name('transmitter'))
    results = db.session.execute(data_list).fetchall()

    # 按照指定格式组织数据
    data = [
        {
            "data": [],
            "name": "Differential Pressure DP(kPa)",
            "threshold": 500,
            "yAxisIndex": 0
        },
        {
            "data": [],
            "name": "Pressure(psi)",
            "threshold": 4600,
            "yAxisIndex": 1
        }
    ]

    # 将查询结果填充到数据结构中
    for row in results:
        dp_value = round(float(row.dp), 2)
        pressure_value = round(float(row.pressure), 2)
        time_value = row.createTime.strftime("%Y-%m-%d %H:%M:%S")

        # 添加DP数据
        data[0]["data"].append({
            "time": time_value,
            "value": dp_value
        })

        # 添加Pressure数据
        data[1]["data"].append({
            "time": time_value,
            "value": pressure_value
        })

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
