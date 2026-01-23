from application import db
from datetime import datetime


class WaterCut(db.Model):
    __tablename__ = 'water_cut'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='记录序号')
    sample_time = db.Column(db.DateTime, nullable=False, comment='数据采集时间')
    water_cut = db.Column(db.Numeric(10, 2), nullable=False, comment='含水率（百分比数值）')

    def to_dict(self):
        return {
            "id": self.id,
            "sample_time": self.sample_time.isoformat() if self.sample_time else None,
            "water_cut": float(self.water_cut),
        }


class FormulaCorrection(db.Model):
    __tablename__ = 'formula_correction'

    # 1. 字段完全对应数据表，类型、约束、注释一一匹配
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    dp = db.Column(db.String(255), nullable=False)
    gVF = db.Column(db.String(255), nullable=False)
    waterCut = db.Column(db.String(255), nullable=False)
    pressure = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False, comment='1=开启，2=关闭')
    updated_time = db.Column(db.DateTime, nullable=False, comment='公式更新时间')

    def to_dict(self):
        return {
            # 基础主键
            "id": self.id,
            # 列表核心字段
            "dp": self.dp,
            "gVF": self.gVF,
            "waterCut": self.waterCut,
            "pressure": self.pressure,
            "status": self.status,
            "updated_time": self.updated_time.isoformat() if self.updated_time else None,
        }


class DeviationComparisonResults(db.Model):
    __tablename__ = 'deviation_comparison_results'

    # 1. 字段完全对应数据表，类型、约束、注释一一匹配
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    current_deviation = db.Column(db.DECIMAL(10, 2), nullable=False, comment='当前偏差（百分比）')
    high_deviation_points = db.Column(db.Integer, nullable=False, comment='高偏差点数')
    correction_applied = db.Column(db.Enum('Yes', 'No'), nullable=False, comment='是否已应用修正')
    stat_time = db.Column(db.DateTime, nullable=False, comment='统计记录生成时间')

    def to_dict(self):
        return {
            "id": self.id,
            "stat_time": self.stat_time.isoformat() if self.stat_time else None,
            "current_deviation": self.current_deviation,
            "high_deviation_points": self.high_deviation_points,
            "correction_applied": self.correction_applied,
        }


class DeviationComparison(db.Model):
    __tablename__ = 'deviation_comparison'

    # 1. 字段完全对应数据表，类型、约束、注释一一匹配
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='记录序号')
    time = db.Column(db.DateTime, nullable=False, comment='数据采集时间')
    differential_pressure = db.Column(db.Numeric(10, 2), nullable=False, comment='压差')
    gas_volume_fraction = db.Column(db.Numeric(10, 2), nullable=False, comment='气体体积分数')
    gas_flow_rate = db.Column(db.Numeric(10, 2), nullable=False, comment='气体流量')
    liquid_flow_rate = db.Column(db.Numeric(10, 2), nullable=False, comment='液体流量')
    oil_flow_rate = db.Column(db.Numeric(10, 2), nullable=False, comment='油流量')
    pressure = db.Column(db.Numeric(10, 2), nullable=False, comment='压力')
    temperature = db.Column(db.Numeric(10, 2), nullable=False, comment='温度')
    water_cut = db.Column(db.Numeric(10, 2), nullable=False, comment='含水率（百分比数值）')
    water_flow_rate = db.Column(db.Numeric(10, 2), nullable=False, comment='水流量')
    status = db.Column(db.Integer, nullable=False, comment='开关状态（1：开；0：关）')

    def to_dict(self):
        return {
            "id": self.id,
            "time": self.time.isoformat() if self.time else None,
            "differential_pressure": float(self.differential_pressure),
            "gas_volume_fraction": float(self.gas_volume_fraction),
            "gas_flow_rate": float(self.gas_flow_rate),
            "liquid_flow_rate": float(self.liquid_flow_rate),
            "oil_flow_rate": float(self.oil_flow_rate),
            "pressure": float(self.pressure),
            "temperature": float(self.temperature),
            "water_cut": float(self.water_cut),
            "water_flow_rate": float(self.water_flow_rate),
            "status": self.status
        }


class DataCorrectionRecord(db.Model):
    __tablename__ = 'correction_record'  # 与MySQL表名完全一致

    # 1. 字段对应数据表，类型/约束/注释一一匹配（补充主键ID，符合示例规范）
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    data_time = db.Column(db.DateTime, nullable=False, comment='数据时间')
    modify_time = db.Column(db.DateTime, nullable=False, comment='修改时间')
    correction_type = db.Column(db.String(20), nullable=False, comment='修正类型')
    field = db.Column(db.String(30), nullable=False, comment='字段名称')  # 与表中`field`字段对应
    original_data = db.Column(db.Numeric(10, 2), nullable=False, comment='原始数据（百分比类存数值，如12.50对应12.50%）')
    modified_data = db.Column(db.Numeric(10, 2), nullable=False, comment='修改后数据')

    def to_dict(self):
        return {
            # 基础主键
            "id": self.id,
            # 核心业务字段（与数据表字段顺序一致，便于维护）
            "data_time": self.data_time.isoformat() if self.data_time else None,
            "modify_time": self.modify_time.isoformat() if self.modify_time else None,
            "correction_type": self.correction_type,
            "field": self.field,
            "original_data": float(self.original_data) if self.original_data else None,  # Numeric转float便于前端处理
            "modified_data": float(self.modified_data) if self.modified_data else None
        }