from application import db
from datetime import datetime

class Log(db.Model):
    __tablename__ = 'audit_logs'

    # 1. 字段完全对应数据表，类型、约束、注释一一匹配
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='日志唯一ID（对应日志序号）')
    log_content = db.Column(db.String(500), nullable=False, comment='日志具体内容（记录系统/设备事件）')
    log_time = db.Column(db.DateTime, nullable=False, comment='日志生成时间')

    def to_dict(self):
        return {
            "id": self.id,
            "log_content": self.log_content,
            "log_time": self.log_time.isoformat() if self.log_time else None,  # 格式化时间
        }
