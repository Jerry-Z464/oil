from enum import IntEnum


class DeviceStatus(IntEnum):
    """设备状态"""
    ONLINE = 0
    OFFLINE = 1

class AlertType(IntEnum):
    """告警类型"""
    DEVICE_OFFLINE = 0
    DATA_GAP = 1
    DATA_MISSING = 2
    DUPLICATE_DATA = 3
    DP_HIGH = 4
    PRESSURE_HIGH = 5
    PRESSURE_LOW = 6
    TEMPERATURE_HIGH = 7
    TEMPERATURE_LOW = 8