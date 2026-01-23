from application import db  # 沿用你项目的db实例

class DataFields(db.Model):
    __tablename__ = 'data_fields'

    # 1. 字段完全对应数据表，类型、约束、注释一一匹配
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='配置项序号')
    field_name = db.Column(db.String(50), nullable=False, comment='字段名（如pressure、temperature）')
    description = db.Column(db.String(200), nullable=False, comment='字段描述（如Device Pressure Value）')
    data_type = db.Column(db.String(50), nullable=False, comment='数据类型（如DECIMAL、BOOLEAN）')
    default_value = db.Column(db.String(50), nullable=False, comment='字段值（如4600、true）')
    unit = db.Column(db.String(20), nullable=False, comment='字段单位（如psi、℃、%）')
    storage_format = db.Column(db.String(50), nullable=False, comment='数据库存储格式（如DECIMAL(10,2)）')
    status = db.Column(db.BigInteger, nullable=False, comment='字段状态（1=Active，0=Inactive）')


    def to_dict(self):
        return {
            "id": self.id,
            "field_name": self.field_name,
            "description": self.description,
            "data_type": self.data_type,
            "default_value": self.default_value,
            "unit": self.unit,
            "storage_format": self.storage_format,
            "status": self.status,
        }