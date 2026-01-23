from application import db
from datetime import datetime

class Alert(db.Model):
    __tablename__ = 'alert'

    # 1. 字段完全对应数据表，类型、约束、注释一一匹配
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='告警ID（唯一标识）')
    device_id = db.Column(db.String(50), nullable=False, comment='设备ID（对应页面Device ID）')
    alert_level = db.Column(db.SmallInteger, nullable=False, comment='告警级别（1=Warning警告，2=Critical严重）')  # MySQL的TINYINT对应Python的SmallInteger
    metric = db.Column(db.String(50), nullable=True, comment='监控指标（Pressure/Temperature等）')
    current_value = db.Column(db.String(50), nullable=False, comment='当前值（数值类型，支持小数）')  # DECIMAL(10,2)对应Numeric
    threshold = db.Column(db.String(50), nullable=False, comment='阈值（比如压力阈值500）')
    suggestion = db.Column(db.String(500), nullable=False, comment='处理建议')
    trigger_time = db.Column(db.DateTime, nullable=False, comment='触发时间')
    notification_status = db.Column(db.SmallInteger, nullable=False, default=0, comment='通知状态（0=未通知，1=已通知）')
    notification_channels = db.Column(db.String(100), nullable=False, comment='通知渠道（多个用逗号分隔，如Email,SMS）')

    def to_dict(self):
        return {
            # 基础主键
            "id": self.id,
            # 列表核心字段（和员工模型字段命名风格对齐，用小写下划线更规范）
            "device_id": self.device_id,
            "alert_level": "Warning" if self.alert_level == 1 else "Critical",
            "metric": self.metric,
            "current_value": self.current_value,
            "threshold": self.threshold,
            "suggestion": self.suggestion,
            # 详情额外字段
            "trigger_time": self.trigger_time,
            "notification_status": "Notified" if self.notification_status == 1 else "Unnotified",
            "notification_channels": self.notification_channels.split(","),
        }


class NotificationSettings(db.Model):
    __tablename__ = 'notification_settings'

    # 1. 字段完全对应数据表，类型、约束、注释一一匹配
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    notification_methods = db.Column(db.String(100), nullable=False, comment='通知方式（多个用逗号分隔，如"1=Email,2=SMS"）')
    alert_suppression_time = db.Column(db.Integer, nullable=False, comment='告警抑制时间（单位：分钟））')
    recipients = db.Column(db.Text, nullable=False, comment='通知接收人（多个用逗号分隔，如"Engineer A (engineer.a@example.com),Admin (admin@example.com)"）')
    created_at = db.Column(db.DateTime, nullable=False, comment='设置创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, comment='设置最后更新时间')

    def to_dict(self):
        return {
            "id": self.id,
            "notification_methods": self.notification_methods,
            "alert_suppression_time": self.alert_suppression_time,
            "recipients": self.recipients,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }