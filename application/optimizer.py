from flask import Blueprint, request
from application import db
from application.base import Result, PageResult
from application.base.AnalysisParam import Param, get_post_data
from application.utils.tools import handle_exceptions
from datetime import datetime
from application.api.models.deviation_comparison import DeviationComparison,DeviationComparisonResults,FormulaCorrection,WaterCut,DataCorrectionRecord
optimizer_bp = Blueprint('optimizer', __name__, url_prefix='/optimizer')


@optimizer_bp.route('/base/results', methods=['GET'])
@handle_exceptions(msg="获取汇总统计类数据失败！")
def get_base_results():
    # 如果需要根据ID查询特定记录
    params = [
        Param(name='id', param_type=int, required=False),  # 设为可选参数
    ]
    query = get_post_data(request, params)

    # 查询所有记录或根据ID查询
    if query.id:
        results = DeviationComparisonResults.query.filter(
            DeviationComparisonResults.id == query.id
        ).all()
    else:
        results = DeviationComparisonResults.query.all()

    # 组装返回数据
    data = [{
        "current_deviation": item.current_deviation,
        "high_deviation_points": item.high_deviation_points,
        "correction_applied": item.correction_applied,
        "stat_time": item.stat_time.isoformat() if item.stat_time else None
    } for item in results]

    return Result.success(data=data)


@optimizer_bp.route('/base/list', methods=['GET'])
@handle_exceptions(msg="获取基础参数列表失败！")
def get_base_list():
    params = [
        Param(name='pageNumber', param_type=int, required=True),
        Param(name='pageSize', param_type=int, required=True),
    ]
    query = get_post_data(request, params)
    page_number = query.pageNumber
    page_size = query.pageSize

    query_obj = WaterCut.query.with_entities(
        WaterCut.id,
        WaterCut.sample_time,
        WaterCut.water_cut
    )

    pagination = query_obj.paginate(page=page_number, per_page=page_size, error_out=False)

    # 3. 组装返回数据
    data = [{
            "id": item[0],
            "sample_time": item[1].isoformat() if item[1] else None,
            "water_cut": float(item[2])
        } for item in pagination.items]
    return PageResult.success(total=pagination.total, page_number=page_number, page_size=page_size,
                              pages=(pagination.total // query.pageSize) + 1, data=data)


@optimizer_bp.route('/base/add', methods=['POST'])
@handle_exceptions(msg="新增基础参数失败！")
def get_base_add():
    params = [
        Param(name='water_cut', param_type=str, required=True),

    ]
    query = get_post_data(request, params)
    new_alarm = WaterCut(
        water_cut=query.water_cut,
        sample_time=datetime.now()
    )

    # 2. 提交到数据库
    db.session.add(new_alarm)
    db.session.commit()

    return Result.success(msg="新增基础参数成功")

@optimizer_bp.route('/base/update', methods=['POST'])
@handle_exceptions(msg="修改基础参数失败！")
def get_base_update():
    params = [
        Param(name='id', param_type=int, required=True),
        Param(name='water_cut', param_type=str, required=True),
    ]
    query = get_post_data(request, params)
    base_id = query.id
    new_water_cut = query.water_cut
    base = WaterCut.query.get_or_404(base_id)
    base.water_cut = new_water_cut
    db.session.commit()
    data = {
        "detail": {
            "status": base.water_cut
        }
    }
    return Result.success(data=data)

@optimizer_bp.route('/base/delete', methods=['POST'])
@handle_exceptions(msg="删除基础参数失败！")
def get_base_delete():
    params = [
        Param(name='id', param_type=int, required=True),
    ]
    query = get_post_data(request, params)
    bash_id = query.id

    # 1. 根据ID查询员工
    employee = WaterCut.query.get_or_404(bash_id)

    # 2. 删除并提交
    db.session.delete(employee)
    db.session.commit()

    return Result.success(msg="删除基础参数成功")


@optimizer_bp.route('/list', methods=['GET'])
@handle_exceptions(msg="获取数据列表失败！")
def get_optimizer_list():
    params = [
        Param(name='pageNumber', param_type=int, required=True),
        Param(name='pageSize', param_type=int, required=True),
        Param(name='status', param_type=int, required=False),  # 设为可选参数
    ]
    query = get_post_data(request, params)
    page_number = query.pageNumber
    page_size = query.pageSize
    status = query.status


    query_obj = DeviationComparison.query
    if status is not None:
        query_obj = query_obj.filter(DeviationComparison.status == status)

    # 2. 分页查询（SQLAlchemy的paginate方法）
    pagination = query_obj.paginate(page=page_number, per_page=page_size, error_out=False)

    # 3. 组装返回数据
    data = {
        "total": pagination.total,  # 总条数
        "pages": pagination.pages,  # 总页数
        "list": [item.to_dict() for item in pagination.items]  # 当前页数据列表
    }
    return Result.success(data=data)


@optimizer_bp.route('/correction/list', methods=['GET'])
@handle_exceptions(msg="获取数据修正记录列表失败！")
def get_correction_record_list():
    # 1. 定义请求参数（仅保留分页必填参数，查询全部无需额外筛选条件）
    params = [
        Param(name='pageNumber', param_type=int, required=True),
        Param(name='pageSize', param_type=int, required=True),
    ]
    query = get_post_data(request, params)
    page_number = query.pageNumber
    page_size = query.pageSize

    query_obj = DataCorrectionRecord.query
    query_obj = query_obj.order_by(DataCorrectionRecord.modify_time.desc())

    pagination = query_obj.paginate(page=page_number, per_page=page_size, error_out=False)

    data = {
        "total": pagination.total,  # 符合条件的总记录数
        "pages": pagination.pages,  # 总页数（自动计算）
        "list": [item.to_dict() for item in pagination.items]
    }

    return Result.success(data=data)


@optimizer_bp.route('/formula', methods=['POST'])
@handle_exceptions(msg="控制公式开关失败！")
def optimizer_formula():
    params = [
        Param(name='id', param_type=int, required=True),
        Param(name='status', param_type=int, required=True),
    ]
    query = get_post_data(request, params)
    base_id = query.id
    new_status = query.status
    base = FormulaCorrection.query.get_or_404(base_id)
    base.status = new_status
    db.session.commit()
    data = {
        "detail": {
            "status": base.status,
            "message": "开关已打开" if base.status == 1 else "开关已关闭" if base.status == 0 else "未知状态"
        }
    }
    return Result.success(data=data)

@optimizer_bp.route('/formula/update', methods=['POST'])
@handle_exceptions(msg="修改公式失败！")
def formula_update():
    params = [
        Param(name='id', param_type=int, required=True),
        Param(name='dp', param_type=str, required=False),
        Param(name='gVF', param_type=str, required=False),
        Param(name='waterCut', param_type=str, required=False),
        Param(name='pressure', param_type=str, required=False),
    ]
    query = get_post_data(request, params)
    base_id = query.id
    base = FormulaCorrection.query.get_or_404(base_id)
    if base.status == 1:
        if hasattr(query, 'dp') and query.dp is not None:
            base.dp = query.dp
        if hasattr(query, 'gVF') and query.gVF is not None:
            base.gVF = query.gVF
        if hasattr(query, 'waterCut') and query.waterCut is not None:
            base.waterCut = query.waterCut
        if hasattr(query, 'pressure') and query.pressure is not None:
            base.pressure = query.pressure
        db.session.commit()

        return Result.success(msg="修改公式成功")
    else:
        return Result.failed(msg="修改公式没有打开！")





