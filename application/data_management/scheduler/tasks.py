"""
定时任务模块
"""
import logging
import time
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from application.data_management.storage.constants import DeviceStatus, AlertType
from application.data_management.storage.database import Database
from application.data_management.storage.settings import SettingManager
from application.data_management.storage.db_models import Device, DeviceData
from application.data_management.modules.alert.alert_manager import AlertManager
from application.data_management.modules.audit.audit_logger import AuditLogger
from application.data_management.modules.audit.event_type import AuditEventType


class ScheduledTasks:
    """定时任务"""

    def __init__(self, db: Database, settings: SettingManager, alert_manager: AlertManager, audit_logger: AuditLogger):
        self.db = db
        self.settings = settings
        self.alert_manager = alert_manager
        self.audit_logger = audit_logger

        self.scheduler = BackgroundScheduler()

    def start(self):
        """启动定时任务"""

        # 每 1 分钟检查设备在线状态
        self.scheduler.add_job(
            self.check_device_online,
            'interval',
            minutes=1,
            id='check_device_online'
        )

        # 每 1 小时检查数据库健康
        self.scheduler.add_job(
            self.check_database_health,
            'interval',
            hours=1,
            id='check_database_health'
        )

        self.scheduler.start()
        logging.info("[定时任务] 已启动")

    def stop(self):
        """停止定时任务"""
        self.scheduler.shutdown()
        logging.info("[定时任务] 已停止")

    def check_device_online(self):
        """检查所有设备在线状态"""

        logging.info(f"[{datetime.now()}] 检查设备在线状态...")

        session = self.db.get_session()

        try:
            threshold_minutes = self.settings.get("OFFLINE_THRESHOLD_MINUTES")
            now = datetime.now()
            offline_threshold = now - timedelta(minutes=threshold_minutes)

            # 查询所有设备
            devices = session.query(Device).all()

            for device in devices:

                # 超时且当前状态是在线
                if device.last_update_time < offline_threshold and device.status == DeviceStatus.ONLINE:
                    # 更新状态
                    device.status = DeviceStatus.OFFLINE

                    # 计算离线时长
                    minutes_offline = (now - device.last_update_time).total_seconds() / 60

                    # 发送告警
                    self.alert_manager.send(
                        device_id=device.id,
                        alert_type=AlertType.DEVICE_OFFLINE,
                        message=f"设备 {device.id} 已离线，{minutes_offline:.0f} 分钟未收到数据",
                    )

                    # 记录审计日志
                    self.audit_logger.log(AuditEventType.ALERT_TRIGGERED, device.id)

                    logging.warning(f"⚠️ 设备 {device.id} 离线")

            session.commit()

        except Exception as e:
            session.rollback()
            logging.error(f"[定时任务] 检查在线状态失败: {e}")
        finally:
            session.close()

    def check_database_health(self):
        """检查数据库健康"""

        logging. info(f"[{datetime.now()}] 检查数据库健康...")

        session = self.db.get_session()

        try:
            # 获取配置
            # 数据上报间隔（秒）
            data_interval_seconds = 60
            # 缺失率阈值
            missing_threshold_percent = self.settings.get("DATA_MISSING_THRESHOLD_PERCENT")

            # 24小时时间范围
            now = int(time.time())
            hours_24_ago = now - 24 * 60 * 60

            # 24小时应有的数据条数
            expected_count = (24 * 60 * 60) // data_interval_seconds

            # 查询所有设备
            devices = session.query(Device).all()

            for device in devices:
                # 统计该设备24小时内的实际数据条数
                actual_count = session.query(DeviceData).filter(
                    DeviceData.device_id == device.id,
                    DeviceData.cmt5_time >= hours_24_ago,
                    DeviceData.cmt5_time <= now
                ).count()

                # 计算缺失率
                missing_count = expected_count - actual_count
                if missing_count < 0:
                    missing_count = 0

                missing_percent = (missing_count / expected_count) * 100

                logging.info(f"设备 {device. id}:  预期 {expected_count} 条, 实际 {actual_count} 条, 缺失率 {missing_percent:.2f}%")

                # 超过阈值，发送告警
                if missing_percent > missing_threshold_percent:
                    sent = self.alert_manager.send(
                        device_id=device.id,
                        alert_type=AlertType.DATA_MISSING,
                        message=f"设备 {device. id} 24小时数据缺失率 {missing_percent:. 2f}%，超过阈值 {missing_threshold_percent}%"
                    )

                    if sent:
                        self. audit_logger.log(AuditEventType.ALERT_TRIGGERED, device. id)

                    logging.warning(f"⚠️ 设备 {device.id} 数据缺失率过高:  {missing_percent:. 2f}%")

        except Exception as e:
            logging.error(f"[定时任务] 检查数据库健康失败:  {e}")
        finally:
            session.close()
