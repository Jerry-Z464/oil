from enum import Enum


class AuditEventType(Enum):
    """审计事件类型"""

    # 优化器相关
    OPTIMIZER_ON = "optimizer_on"
    OPTIMIZER_OFF = "optimizer_off"

    # 样本相关
    SAMPLE_INPUT = "sample_input"

    # 偏差计算
    DEVIATION_CALC = "deviation_calc"

    # 告警相关
    ALERT_TRIGGERED = "alert_triggered"