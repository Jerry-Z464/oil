from application.data_management.models.well_data import WellData
from application.data_management.modules.alert.alert_manager import AlertManager
from application.data_management.modules.audit.audit_logger import AuditLogger
from application.data_management.modules.audit.event_type import AuditEventType
from application.data_management.storage.database import Database
from application.data_management.storage.db_models import DeviceData
from application.data_management.storage.constants import AlertType


class DatabaseHealthMonitor:

    def __init__(self, db: Database, alert_manager: AlertManager, audit_logger: AuditLogger):
        self.db = db
        self.alert_manager = alert_manager
        self.audit_logger = audit_logger

    def process(self, device_id: str, well_data: WellData):
        """检查数据健康并存储"""

        session = self.db. get_session()

        try:
            # 重复数据检查
            existing = session.query(DeviceData).filter_by(
                device_id=device_id,
                cmt5_time=well_data.cmt5_time,
                dP=well_data.dP,
                gVF=well_data.gVF,
                gasFlowRate=well_data.gasFlowRate,
                liquidFlowRate=well_data. liquidFlowRate,
                oilFlowRate=well_data.oilFlowRate,
                pressure=well_data.pressure,
                temperature=well_data.temperature,
                waterCut=well_data.waterCut,
                waterFlowRate=well_data.waterFlowRate,
            ).first()

            if existing is not None:
                # 重复数据，发告警，不存储
                self._send_alert(device_id, AlertType.DUPLICATE_DATA,
                    f"设备 {device_id} 检测到重复数据")
                return

            # 不重复，存储数据
            self._save_data(session, device_id, well_data)

        except Exception as e:
            session.rollback()
            print(f"[数据库健康检查] 处理失败: {e}")
        finally:
            session.close()

    def _save_data(self, session, device_id: str, well_data:  WellData):
        """保存数据"""
        data = DeviceData(
            device_id=device_id,
            cmt5_time=well_data.cmt5_time,
            dP=well_data.dP,
            gVF=well_data. gVF,
            gasFlowRate=well_data. gasFlowRate,
            liquidFlowRate=well_data.liquidFlowRate,
            oilFlowRate=well_data.oilFlowRate,
            pressure=well_data.pressure,
            temperature=well_data.temperature,
            waterCut=well_data.waterCut,
            waterFlowRate=well_data.waterFlowRate,
        )
        session.add(data)
        session.commit()

    def _send_alert(self, device_id:  str, alert_type: AlertType, message: str):
        """发送告警"""
        sent = self.alert_manager.send(device_id, alert_type, message)
        if sent:
            self.audit_logger.log(AuditEventType.ALERT_TRIGGERED, device_id)