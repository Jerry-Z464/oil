from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
from enum import Enum
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import Config
from models.data_models import WellDataPoint, Alert, AlertType, DeviceStatus
from analyzer import DataAnalyzer

logger = logging.getLogger(__name__)


class AlertManager:
    """告警管理器"""

    def __init__(self, config: Config):
        self.config = config
        self.active_alerts = {}  # alert_type: last_trigger_time
        self.sent_alerts = {}  # 已发送告警缓存
        self.analyzer = DataAnalyzer(config)

    def check_uptime(self, device_id: str, last_data_time: datetime) -> Optional[Alert]:
        """检查在线状态"""
        time_since_last = datetime.now() - last_data_time

        if time_since_last > self.config.UPTIME_ALERT_THRESHOLD:
            return self._create_alert(
                alert_type=AlertType.UPTIME,
                device_id=device_id,
                message=f"设备 {device_id} 超过 {self.config.UPTIME_ALERT_THRESHOLD} 分钟无数据",
                severity="critical"
            )
        return None

    def check_database_health(self, device_id: str) -> List[Alert]:
        """检查数据库健康"""
        alerts = []

        # 检查数据丢失
        data_loss_rate = self.analyzer.calculate_data_loss_rate(device_id)
        if data_loss_rate > self.config.DATA_LOSS_THRESHOLD:
            alerts.append(self._create_alert(
                alert_type=AlertType.DATA_LOSS,
                device_id=device_id,
                message=f"设备 {device_id} 数据丢失率 {data_loss_rate:.1%} 超过阈值 {self.config.DATA_LOSS_THRESHOLD:.1%}",
                severity="warning"
            ))

        return alerts

    def check_transmitter_thresholds(self, data_point: WellDataPoint) -> Optional[Alert]:
        """检查变送器阈值"""
        if data_point.dp_kpa > self.config.DP_THRESHOLD_KPA:
            return self._create_alert(
                alert_type=AlertType.TRANSMITTER_THRESHOLD,
                device_id=data_point.device_id,
                message=f"设备 {data_point.device_id} 差压 {data_point.dp_kpa:.1f}kPa 超过阈值 {self.config.DP_THRESHOLD_KPA}kPa",
                severity="warning"
            )

        if data_point.pressure_psi > self.config.PRESSURE_THRESHOLD_PSI:
            return self._create_alert(
                alert_type=AlertType.TRANSMITTER_THRESHOLD,
                device_id=data_point.device_id,
                message=f"设备 {data_point.device_id} 压力 {data_point.pressure_psi:.1f}psi 超过阈值 {self.config.PRESSURE_THRESHOLD_PSI}psi",
                severity="warning"
            )

        return None

    def check_temperature_flatline(self, device_id: str) -> Optional[Alert]:
        """检查温度平线"""
        if self.analyzer.check_temperature_flatline(device_id, 10):
            return self._create_alert(
                alert_type=AlertType.TEMPERATURE_FLATLINE,
                device_id=device_id,
                message=f"设备 {device_id} 温度连续10分钟无变化",
                severity="warning"
            )
        return None

    def _create_alert(self, alert_type: AlertType, device_id: str,
                      message: str, severity: str) -> Alert:
        """创建告警对象"""
        alert_id = f"{alert_type.value}_{device_id}_{datetime.now().timestamp()}"

        return Alert(
            alert_id=alert_id,
            alert_type=alert_type,
            device_id=device_id,
            timestamp=datetime.now(),
            message=message,
            severity=severity,
            recipients=self.config.ALERT_RECIPIENTS
        )

    def should_send_alert(self, alert: Alert) -> bool:
        """检查是否应该发送告警（重复抑制）"""
        alert_key = f"{alert.alert_type.value}_{alert.device_id}"

        if alert_key in self.sent_alerts:
            last_sent = self.sent_alerts[alert_key]
            if datetime.now() - last_sent < self.config.ALERT_COOLDOWN:
                return False

        return True

    def send_alert(self, alert: Alert):
        """发送告警"""
        if not self.should_send_alert(alert):
            logger.debug(f"Alert suppressed due to cooldown: {alert.alert_id}")
            return

        try:
            # 发送邮件（示例）
            self._send_email_alert(alert)

            # 发送短信（需要实现）
            # self._send_sms_alert(alert)

            # 记录已发送
            alert_key = f"{alert.alert_type.value}_{alert.device_id}"
            self.sent_alerts[alert_key] = datetime.now()

            logger.info(f"Alert sent: {alert.alert_id} - {alert.message}")

        except Exception as e:
            logger.error(f"Failed to send alert {alert.alert_id}: {e}")

    def _send_email_alert(self, alert: Alert):
        """发送邮件告警"""
        # 这里需要配置SMTP服务器
        msg = MIMEMultipart()
        msg['From'] = 'alerts@oilwell-monitoring.com'
        msg['To'] = ', '.join(alert.recipients)
        msg['Subject'] = f"Oil Well Alert: {alert.alert_type.value}"

        body = f"""
        Alert Details:
        --------------
        Device ID: {alert.device_id}
        Alert Type: {alert.alert_type.value}
        Time: {alert.timestamp}
        Severity: {alert.severity}
        Message: {alert.message}

        Please check the system immediately.
        """

        msg.attach(MIMEText(body, 'plain'))

        # 发送邮件（需要配置SMTP）
        # with smtplib.SMTP('smtp.server.com', 587) as server:
        #     server.starttls()
        #     server.login('username', 'password')
        #     server.send_message(msg)

    def process_data_point(self, data_point: WellDataPoint) -> List[Alert]:
        """处理数据点，检查所有告警条件"""
        alerts = []

        # 添加数据到分析器
        self.analyzer.add_data_point(data_point.device_id, data_point)

        # 检查各种告警条件
        alerts.extend(self.check_database_health(data_point.device_id))

        threshold_alert = self.check_transmitter_thresholds(data_point)
        if threshold_alert:
            alerts.append(threshold_alert)

        temp_alert = self.check_temperature_flatline(data_point.device_id)
        if temp_alert:
            alerts.append(temp_alert)

        # 发送所有告警
        for alert in alerts:
            self.send_alert(alert)

        return alerts