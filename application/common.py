from enum import Enum


class DeviceStatus(Enum):
    NORMAL = "normal"
    WARNING = "warning"
    ALERT = "alert"
    OFFLINE = "offline"


class AlarmType(Enum):
    UPTIME = "uptime_alert"
    DATABASE_HEALTH = "database_health_alert"
    TRANSMITTER_THRESHOLD = "transmitter_threshold_alert"
    TEMPERATURE_FLATLINE = "temperature_flatline_alert"
    DATA_LOSS = "data_loss_alert"
    DUPLICATE_DATA = "duplicate_data_alert"