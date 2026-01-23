"""
变送器监控模块
"""

from application.data_management.models.well_data import WellData
from application.data_management.modules.alert.alert_manager import AlertManager
from application.data_management.modules.audit.audit_logger import AuditLogger
from application.data_management.modules.audit.event_type import AuditEventType
from application.data_management.storage.database import Database
from application.data_management.storage.constants import AlertType
from application.data_management.storage.settings import SettingManager


class TransmitterMonitor:
    """变送器监控"""

    def __init__(self, db: Database, setting_manager: SettingManager, alert_manager: AlertManager, audit_logger: AuditLogger):
        self.db = db
        self.setting_manager = setting_manager
        self.alert_manager = alert_manager
        self.audit_logger = audit_logger

    def process(self, device_id: str, well_data: WellData):
        """检查变送器参数"""

        dp_threshold = int(self.setting_manager.get("DIFFERENTIAL_PRESSURE_THRESHOLD"))

        # 检查差压是否超出阈值
        if well_data.dP > dp_threshold:
            self._send_alert(device_id, AlertType.DP_HIGH, f"设备 {device_id} 差压过高: {well_data.dP} kPa。阈值: {dp_threshold} kPa")

    def _send_alert(self, device_id: str, alert_type: AlertType, message: str):
        """发送告警"""
        sent = self.alert_manager.send(device_id, alert_type, message)
        if sent:
            self.audit_logger.log(AuditEventType.ALERT_TRIGGERED, device_id)
