import logging
import time

from application.data_management.storage.database import Database
from application.data_management.storage.db_models import AuditLog
from application.data_management.modules.audit.event_type import AuditEventType


class AuditLogger:
    """审计日志记录器"""

    def __init__(self, db: Database):
        self.db = db

    def log(self, event_type: AuditEventType, device_id: str):

        session = self.db.get_session()

        try:
            log = AuditLog(
                timestamp=int(time.time()),
                event_type=event_type.value,
                device_id=device_id
            )
            session.add(log)
            session.commit()

        except Exception as e:
            session.rollback()
            logging.error(f"[审计日志] 记录失败: {e}")
        finally:
            session.close()
