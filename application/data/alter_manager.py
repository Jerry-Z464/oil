# alert_manager.py
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class AlertManager:
    def __init__(self, config):
        self.config = config
        self.data_store = TimeWindowDataStore(window_hours=24)

        # 告警抑制管理
        self.notification_cooldown = timedelta(minutes=30)
        self.last_notification_time: Dict[Tuple[str, AlertType], datetime] = {}

        # 中断时间段记录
        self.interruption_periods: Dict[str, List[Tuple[datetime, datetime]]] = defaultdict(list)
        self.last_data_time: Dict[str, datetime] = {}

        # 温度平线检测
        self.temperature_history: Dict[str, List[Tuple[datetime, float]]] = defaultdict(list)

    def process_data_point(self, device_id: str, data_point: DataPoint) -> List[Alert]:
        """处理数据点，返回所有触发的告警"""
        alerts = []

        # 1. 存储数据
        self.data_store.add_data(device_id, data_point)

        # 2. 更新最后数据时间（用于中断检测）
        self._update_last_data_time(device_id, data_point.timestamp)

        # 3. 检查所有告警条件
        # 3.1 重复数据检测
        if self._check_duplicate_data(device_id, data_point):
            alerts.append(self._create_alert(
                device_id, AlertType.DUPLICATE_DATA,
                f"设备 {device_id} 检测到重复数据",
                "warning"
            ))

        # 3.2 数据缺失检测
        loss_rate = self.data_store.calculate_data_loss_rate(device_id)
        if loss_rate > self.config.data_missing_threshold:  # 3%
            alerts.append(self._create_alert(
                device_id, AlertType.DATA_MISSING,
                f"设备 {device_id} 数据缺失率 {loss_rate:.1%} > 3%",
                "warning"
            ))

        # 3.3 变送器阈值检测
        if data_point.dp > self.config.dp_threshold:  # 500 kPa
            alerts.append(self._create_alert(
                device_id, AlertType.DP_THRESHOLD,
                f"设备 {device_id} 差压 {data_point.dp:.1f}kPa > 500kPa",
                "critical"
            ))

        if data_point.pressure > self.config.pressure_threshold:  # 4600 psi
            alerts.append(self._create_alert(
                device_id, AlertType.PRESSURE_THRESHOLD,
                f"设备 {device_id} 压力 {data_point.pressure:.1f}psi > 4600psi",
                "critical"
            ))

        # 3.4 温度平线检测
        if self._check_temperature_flatline(device_id, data_point):
            alerts.append(self._create_alert(
                device_id, AlertType.TEMPERATURE_FLATLINE,
                f"设备 {device_id} 温度连续10分钟无变化",
                "warning"
            ))

        # 4. 应用告警抑制
        alerts = self._apply_notification_suppression(alerts)

        # 5. 发送需要通知的告警
        for alert in alerts:
            if alert.should_notify:
                self._send_notification(alert)

        return alerts

    def _check_duplicate_data(self, device_id: str, new_point: DataPoint) -> bool:
        """检查重复数据"""
        recent_data = self.data_store.get_data_in_window(
            device_id,
            start_time=datetime.now() - timedelta(minutes=5)  # 检查最近5分钟
        )

        for point in recent_data[-10:]:  # 检查最近10个点
            if (abs((point.timestamp - new_point.timestamp).total_seconds()) < 1 and
                    point.content_hash() == new_point.content_hash()):
                return True
        return False

    def _check_temperature_flatline(self, device_id: str,
                                    current_point: DataPoint) -> bool:
        """检查温度平线"""
        # 维护最近10分钟的温度记录
        history = self.temperature_history[device_id]
        now = datetime.now()

        # 添加当前温度
        history.append((now, current_point.temperature))

        # 清理10分钟前的数据
        cutoff = now - timedelta(minutes=10)
        self.temperature_history[device_id] = [
            (ts, temp) for ts, temp in history if ts >= cutoff
        ]

        # 检查是否有足够数据
        if len(history) < 10:  # 每分钟一个点，需要10个点
            return False

        # 检查温度变化
        temps = [temp for _, temp in history[-10:]]
        if all(abs(t - temps[0]) < 0.01 for t in temps):  # 变化小于0.01度
            return True

        return False

    def _update_last_data_time(self, device_id: str, timestamp: datetime):
        """更新最后数据时间，检测中断"""
        last_time = self.last_data_time.get(device_id)

        if last_time:
            gap = timestamp - last_time
            if gap > timedelta(minutes=5):  # 5分钟无数据认为中断开始
                # 记录中断开始时间
                self.interruption_periods[device_id].append((last_time, timestamp))

        self.last_data_time[device_id] = timestamp

    def _apply_notification_suppression(self, alerts: List[Alert]) -> List[Alert]:
        """应用通知抑制策略"""
        suppressed_alerts = []

        for alert in alerts:
            key = (alert.device_id, alert.alert_type)
            last_time = self.last_notification_time.get(key)

            if last_time and (datetime.now() - last_time) < self.notification_cooldown:
                # 30分钟内同类型告警不发送通知，但记录告警
                alert.should_notify = False
                suppressed_alerts.append(alert)
            else:
                # 可以发送通知，更新时间
                self.last_notification_time[key] = datetime.now()
                suppressed_alerts.append(alert)

        return suppressed_alerts

    def _create_alert(self, device_id: str, alert_type: AlertType,
                      message: str, severity: str) -> Alert:
        """创建告警对象"""
        return Alert(
            alert_id=f"{alert_type.value}_{device_id}_{datetime.now().timestamp()}",
            alert_type=alert_type,
            device_id=device_id,
            timestamp=datetime.now(),
            message=message,
            severity=severity
        )

    def _send_notification(self, alert: Alert):
        """发送通知（邮件等）"""
        try:
            # 这里实现邮件发送逻辑
            logger.info(f"发送告警通知: {alert.message}")
            alert.notified_at = datetime.now()

            # 邮件发送示例
            if self.config.smtp_enabled:
                self._send_email(alert)

        except Exception as e:
            logger.error(f"发送通知失败: {e}")

    def get_interruption_periods(self, device_id: str) -> List[Tuple[datetime, datetime]]:
        """获取24小时内的中断时间段"""
        cutoff = datetime.now() - timedelta(hours=24)
        periods = self.interruption_periods.get(device_id, [])
        return [(start, end) for start, end in periods if end >= cutoff]