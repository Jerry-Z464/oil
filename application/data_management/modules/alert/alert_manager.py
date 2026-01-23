import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict

from application.data_management.storage.database import Database
from application.data_management.storage.settings import SettingManager
from application.data_management.storage.db_models import Alert
from application.data_management.storage.constants import AlertType


class AlertManager:
    """告警管理器"""

    def __init__(self, db: Database, settings: SettingManager):
        self.db = db
        self.settings = settings
        self._suppression_cache: Dict[str, datetime] = {}

    def send(self, device_id: str, alert_type: AlertType, message: str) -> bool:
        """发送告警"""

        if self._is_suppressed(device_id, alert_type):
            return False

        self._save_alert(device_id, alert_type, message)
        self._send_email(device_id, alert_type, message)
        self._update_suppression(device_id, alert_type)

        return True

    def _is_suppressed(self, device_id: str, alert_type: AlertType) -> bool:
        """检查是否在抑制期内"""
        key = f"{device_id}:{alert_type.value}"

        if key not in self._suppression_cache:
            return False

        suppression_minutes = self.settings.get("ALERT_REPETITION_INHIBITION_TIME")
        last_sent = self._suppression_cache[key]
        suppression_until = last_sent + timedelta(minutes=suppression_minutes)

        return datetime.now() < suppression_until

    def _update_suppression(self, device_id: str, alert_type: AlertType):
        """更新抑制缓存"""
        key = f"{device_id}:{alert_type.value}"
        self._suppression_cache[key] = datetime.now()

    def _save_alert(self, device_id: str, alert_type: AlertType, message: str):
        """保存告警到数据库"""

        session = self.db.get_session()

        try:
            alert = Alert(
                device_id=device_id,
                alert_type=alert_type.value,
                message=message,
                created_at=int(time.time())
            )
            session.add(alert)
            session.commit()

        except Exception as e:
            session.rollback()
            print(f"[告警] 保存失败: {e}")
        finally:
            session.close()

    def _send_email(self, device_id: str, alert_type: AlertType, message: str) -> bool:
        """发送邮件"""

        smtp_server = self.settings.get("ALERT_SMTP_HOST")
        smtp_port = self.settings.get("ALERT_SMTP_PORT")
        smtp_username = self.settings.get("ALERT_SMTP_USER")
        smtp_password = self.settings.get("ALERT_SMTP_PASSWORD")
        sender_email = self.settings.get("ALERT_SMTP_SENDER")
        receivers = self.settings.get("ALERT_SMTP_RECEIVERS")

        if not receivers:
            print(f"[告警] 未配置收件人，跳过发送: {message}")
            return False

        subject = f"[油井告警] {device_id} - {alert_type.name}"

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ', '.join(receivers)
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain', 'utf-8'))

            # TLS
            # with smtplib.SMTP(smtp_server, smtp_port) as server:
            #     server.starttls()
            #     server.login(smtp_username, smtp_password)
            #     server.sendmail(sender_email, receivers, msg.as_string())

            # SSL
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receivers, msg.as_string())

            print(f"[告警] 邮件发送成功: {message}")
            return True

        except Exception as e:
            print(f"[告警] 邮件发送失败: {e}")
            return False
