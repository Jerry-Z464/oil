from flask import Blueprint, request
from sqlalchemy import text
from application import db
from application.base import Result, DataResult, PageResult
from application.base.AnalysisParam import Param, get_post_data
from application.entity import WellData
from application.utils.database import render_sql, file_name
from application.utils.tools import handle_exceptions

data_bp = Blueprint('data', __name__, url_prefix='/data')


@data_bp.route('list', methods=['GET'])
@handle_exceptions(msg="获取数据失败")
def get_data_list():
    params = [
        Param(name='code', param_type=str, required=False),
        Param(name='pageSize', param_type=int, required=True),
        Param(name='pageNumber', param_type=int, required=True)
    ]
    query = get_post_data(request, params)
    data_list = render_sql(file_name('data_list'), {
        'confined': (query.pageNumber - 1) * query.pageSize,
        'offset': query.pageSize
    })
    results = db.session.execute(data_list).fetchall()
    # 将结果转换为 JSON 格式并返回
    items_json = [{'id': item.id,
                   'code': item.code,
                   'dp': item.dp,
                   'gvf': item.gvf,
                   'gas_flow_rate': item.gasFlowRate,
                   'liquid_flow_rate': item.liquidFlowRate,
                   'oil_flow_rate': item.oilFlowRate,
                   'pressure': item.pressure,
                   'temperature': item.temperature,
                   'water_cut': item.waterCut,
                   'water_flow_rate': item.waterFlowRate,
                   'status': item.status,
                   'create_time': item.createTime.strftime("%Y-%m-%d %H:%M:%S")} for item in results]
    # 执行总数查询
    total_result = db.session.execute(text("SELECT FOUND_ROWS() AS total"))
    total = total_result.fetchone()[0]
    return PageResult.success(total=total, page_number=query.pageNumber, page_size=query.pageSize,
                              pages=(total // query.pageSize) + 1, data=items_json)


@data_bp.route('optimizer', methods=['GET'])
@handle_exceptions(msg="获取数据失败")
def data_optimizer():
    params = [
        Param(name='id', param_type=int, required=True)
    ]
    query = get_post_data(request, params)
    data = WellData.query.filter_by(id=query.id).one_or_none()
    if data is None:
        return Result.failed(msg="数据不存在！")
    # 将结果转换为 JSON 格式并返回
    items_json = [{'updateData': data.water_cut_optimizer,
                  'origin': data.water_cut,
                  'field': '含水率',
                  'updateType': 0,
                  'dataTime': data.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                  'updateTime': data.create_time.strftime("%Y-%m-%d %H:%M:%S")}]
    return DataResult.success(data=items_json)
