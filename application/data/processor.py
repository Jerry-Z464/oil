import time
from application import app, logger, db
from application.entity import DeviceData
# from application.data_management.models.well_data import WellData
# from application.data_management.modules.audit.audit_logger import AuditLogger
# from application.data_management.modules.alert.alert_manager import AlertManager
# from application.data_management.modules.monitoring.db_health import DatabaseHealthMonitor
# from application.data_management.modules.monitoring.online_status import OnlineStatusMonitor
# from application.data_management.modules.monitoring.transmitter import TransmitterMonitor
# from application.data_management.modules.optimizer.optimizer_manager import OptimizerManager
# from application.data_management.storage.database import Database
# from application.data_management.storage.settings import SettingManager
# from application.data.collector import read_modbus_registers


def process_data(measurements):
    try:
        # 数据库健康检查
        # 存储设备数据
        device_data = DeviceData(code=measurements["wellCode"], dp=measurements["dp"], gvf=measurements["GVF"],
                                 gas_flow_rate=measurements["gasFlowRate"],
                                 liquid_flow_rate=measurements["liquidFlowRate"],
                                 oil_flow_rate=measurements["oilFlowRate"],
                                 pressure=measurements["pressure"],
                                 temperature=measurements["temperature"],
                                 water_cut=measurements["waterCut"],
                                 water_flow_rate=measurements["waterFlowRate"])
        db.session.add(device_data)
        db.commit()
    except Exception as e:
        logger.error("采集数据失败：{}".format(str(e)))

# class DataProcessor:
#
#     def __init__(self, db: Database, settings: SettingManager):
#         self.db = db
#         self.settings = settings
#
#         self.alert_manager = AlertManager(db, settings)
#         self.audit_logger = AuditLogger(db)
#
#         self.online_monitor = OnlineStatusMonitor(db)
#         self.db_health_monitor = DatabaseHealthMonitor(db, self.alert_manager, self.audit_logger)
#         self.transmitter_monitor = TransmitterMonitor(db, settings, self.alert_manager, self.audit_logger)
#         self.optimizer_manager = OptimizerManager(db)
#
#     def process(self, device_id: str, data: WellData) -> WellData:
#         """处理单条数据的完整流程"""
#
#         self.online_monitor.process(device_id, data)
#
#         self.db_health_monitor.process(device_id, data)
#
#         self.transmitter_monitor.process(device_id, data)
#
#         optimizer = self.optimizer_manager.get(device_id)
#         # processed_data 为优化器修正后的数据
#         processed_data = optimizer.process(data)
#
#         return data
