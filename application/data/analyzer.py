from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import deque, defaultdict
import statistics
from application import logger
from application.data.models import DataPoint


class TimeWindowDataStore:
    """时间窗口数据存储，支持滑动窗口清理"""

    def __init__(self, window_hours: int = 24):
        self.window_hours = window_hours
        # 按设备存储数据点
        self.data: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        # 数据统计缓存
        self.stats_cache: Dict[str, dict] = {}
        self.cache_valid_minutes = 5
        self.last_update_time: Dict[str, datetime] = {}

    def add_data(self, device_id: str, data_point: DataPoint):
        """添加数据点并清理旧数据"""
        buffer = self.data[device_id]
        buffer.append(data_point)
        self._clean_old_data(device_id)
        self.stats_cache.pop(device_id, None)  # 使缓存失效

    def _clean_old_data(self, device_id: str):
        """清理超过时间窗口的旧数据"""
        cutoff_time = datetime.now() - timedelta(hours=self.window_hours)
        buffer = self.data[device_id]

        # 从左侧移除旧数据
        while buffer and buffer[0].timestamp < cutoff_time:
            buffer.popleft()

    def get_data_in_window(self, device_id: str,
                           start_time: datetime = None,
                           end_time: datetime = None) -> List[DataPoint]:
        """获取指定时间窗口内的数据"""
        if device_id not in self.data:
            return []

        if start_time is None:
            start_time = datetime.now() - timedelta(hours=self.window_hours)
        if end_time is None:
            end_time = datetime.now()

        return [
            point for point in self.data[device_id]
            if start_time <= point.timestamp <= end_time
        ]

    def calculate_data_loss_rate(self, device_id: str,
                                 expected_interval_minutes: int = 1) -> float:
        """计算数据丢失率"""
        data_points = list(self.data[device_id])
        if len(data_points) < 2:
            return 1.0

        # 按时间排序
        sorted_points = sorted(data_points, key=lambda x: x.timestamp)

        # 计算总时间范围和期望数据点数
        total_minutes = self.window_hours * 60
        expected_count = total_minutes / expected_interval_minutes

        # 统计实际数据点
        actual_count = len(sorted_points)

        if expected_count == 0:
            return 0.0

        loss_rate = max(0.0, 1 - (actual_count / expected_count))
        return round(loss_rate, 4)

    def get_water_cut_average(self, device_id: str,
                              hours: int = 24) -> Optional[float]:
        """获取指定小时数的含水率平均值"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        data_points = [
            point for point in self.data[device_id]
            if point.timestamp >= cutoff_time
        ]

        if not data_points:
            return None

        return statistics.mean(point.water_cut for point in data_points)