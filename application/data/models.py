from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class AlertType(Enum):
    # 基础在线状态告警
    UPTIME_OFFLINE = "uptime_offline"  # 设备离线（数据中断）
    UPTIME_RECOVERED = "uptime_recovered"  # 设备恢复在线

    # 数据库健康告警
    DATA_INTERRUPTION = "data_interruption"  # 数据中断时间段
    DUPLICATE_DATA = "duplicate_data"  # 重复数据
    DATA_MISSING = "data_missing"  # 数据缺失

    # 变送器阈值告警
    DP_THRESHOLD = "dp_threshold"  # 差压超限
    PRESSURE_THRESHOLD = "pressure_threshold"  # 压力超限

    # 温度告警
    TEMPERATURE_FLATLINE = "temperature_flatline"  # 温度平线


@dataclass
class DataPoint:
    device_id: str
    timestamp: datetime
    dp: float  # 差压 (kPa)
    pressure: float  # 压力 (psi)
    temperature: float  # 温度 (℃)
    water_cut: float  # 含水率 (%)
    liquid_flow: float  # 液体流量
    water_flow: float  # 水流量
    oil_flow: float  # 油流量
    gas_flow: float  # 气流量

    # 用于重复检测的哈希值
    def content_hash(self) -> str:
        return f"{self.dp:.2f}_{self.pressure:.2f}_{self.temperature:.2f}_{self.water_cut:.2f}"


@dataclass
class Alert:
    alert_id: str
    alert_type: AlertType
    device_id: str
    timestamp: datetime
    message: str
    severity: str  # "warning", "critical"
    should_notify: bool = True  # 是否发送通知
    notified_at: Optional[datetime] = None