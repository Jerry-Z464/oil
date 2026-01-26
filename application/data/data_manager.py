from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Deque
from collections import deque, defaultdict
import statistics
import logging
from application.data.models import DataPoint

logger = logging.getLogger(__name__)


class TimeWindowDataManager:
    """统一管理24小时窗口数据，避免频繁数据库查询"""

    def __init__(self, config):
        self.config = config
        # 存储24小时内的数据点
        self.data_points: Dict[str, Deque] = defaultdict(lambda: deque(maxlen=1440))  # 假设1分钟一个点，最多1440个
        # 最后数据时间（用于在线检测）
        self.last_data_times: Dict[str, datetime] = {}
        # 中断记录
        self.interruption_periods: Dict[str, List[Tuple[datetime, datetime]]] = defaultdict(list)
        # 温度历史（用于平线检测）
        self.temperature_history: Dict[str, List[Tuple[datetime, float]]] = defaultdict(list)

    def add_data_point(self, device_id: str, data_point: 'DataPoint'):
        """添加数据点并自动清理24小时前的数据"""
        current_time = datetime.now()

        # 检查是否中断（超过5分钟无数据）
        if device_id in self.last_data_times:
            time_gap = current_time - self.last_data_times[device_id]
            if time_gap > timedelta(minutes=5):
                # 记录中断
                self.interruption_periods[device_id].append(
                    (self.last_data_times[device_id], current_time)
                )
                # 清理24小时前的中断记录
                cutoff = current_time - timedelta(hours=24)
                self.interruption_periods[device_id] = [
                    (start, end) for start, end in self.interruption_periods[device_id]
                    if end >= cutoff
                ]

        # 存储数据点
        self.data_points[device_id].append(data_point)
        self.last_data_times[device_id] = current_time

        # 维护温度历史（用于平线检测）
        self._update_temperature_history(device_id, current_time, data_point.temperature)

    def _update_temperature_history(self, device_id: str, timestamp: datetime, temperature: float):
        """维护10分钟温度历史"""
        history = self.temperature_history[device_id]
        history.append((timestamp, temperature))

        # 保留最近10分钟的数据
        cutoff = timestamp - timedelta(minutes=10)
        self.temperature_history[device_id] = [
            (ts, temp) for ts, temp in history if ts >= cutoff
        ]

    def get_24h_data(self, device_id: str) -> List['DataPoint']:
        """获取24小时内数据"""
        cutoff = datetime.now() - timedelta(hours=24)
        return [dp for dp in self.data_points.get(device_id, [])
                if dp.timestamp >= cutoff]

    def calculate_data_loss_rate(self, device_id: str) -> float:
        """计算24小时内数据缺失率"""
        data_points = self.get_24h_data(device_id)

        # 期望1440个点（24小时 * 60分钟）
        expected_count = 1440
        actual_count = len(data_points)

        if expected_count == 0:
            return 0.0

        loss_rate = max(0.0, 1 - (actual_count / expected_count))
        return round(loss_rate, 4)

    def get_duplicate_data_count(self, device_id: str,
                                 window_minutes: int = 5) -> int:
        """检查最近window_minutes内的重复数据"""
        cutoff = datetime.now() - timedelta(minutes=window_minutes)
        recent_data = [dp for dp in self.data_points.get(device_id, [])
                       if dp.timestamp >= cutoff]

        # 使用集合检测重复
        seen = set()
        duplicates = 0

        for dp in recent_data:
            key = (dp.timestamp, dp.content_hash())
            if key in seen:
                duplicates += 1
            else:
                seen.add(key)

        return duplicates

    def check_temperature_flatline(self, device_id: str) -> bool:
        """检查温度是否连续10分钟无变化"""
        history = self.temperature_history.get(device_id, [])

        if len(history) < 10:  # 需要至少10个数据点
            return False

        # 检查最后10个点的温度变化
        temps = [temp for _, temp in history[-10:]]
        if len(temps) < 10:
            return False

        # 检查是否所有温度值都相同（精确到两位小数）
        first_temp = round(temps[0], 2)
        for temp in temps[1:]:
            if round(temp, 2) != first_temp:
                return False

        return True

    def get_water_cut_24h_avg(self, device_id: str) -> Optional[float]:
        """获取24小时含水率平均值"""
        data_points = self.get_24h_data(device_id)

        if not data_points:
            return None

        water_cuts = [dp.water_cut for dp in data_points]
        return statistics.mean(water_cuts)

    def get_last_data_time(self, device_id: str) -> Optional[datetime]:
        """获取最后数据时间"""
        return self.last_data_times.get(device_id)