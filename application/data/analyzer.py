from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import statistics
import logging
from collections import deque, defaultdict
from application import logger
from config import Config
from models.data_models import WellDataPoint, WaterCutSample


class DataAnalyzer:
    """数据分析器"""

    def __init__(self, config: Config):
        self.config = config
        self.data_buffer = defaultdict(lambda: deque(maxlen=1440))  # 存储最近24小时数据
        self.rolling_stats = defaultdict(dict)  # 滚动统计

    def add_data_point(self, device_id: str, data_point: WellDataPoint):
        """添加数据点到分析器"""
        if data_point:
            self.data_buffer[device_id].append(data_point)
            self._update_rolling_stats(device_id, data_point)

    def _update_rolling_stats(self, device_id: str, data_point: WellDataPoint):
        """更新滚动统计"""
        if device_id not in self.rolling_stats:
            self.rolling_stats[device_id] = {
                'wc_sum': 0.0,
                'count': 0,
                'last_update': None
            }

        stats = self.rolling_stats[device_id]
        stats['wc_sum'] += data_point.water_cut
        stats['count'] += 1
        stats['last_update'] = datetime.now()

        # 清理超过24小时的数据
        self._clean_old_data(device_id)

    def _clean_old_data(self, device_id: str):
        """清理超过24小时的旧数据"""
        cutoff_time = datetime.now() - self.config.WC_ROLLING_WINDOW
        buffer = self.data_buffer[device_id]

        # 移除旧数据点
        while buffer and buffer[0].timestamp < cutoff_time:
            old_point = buffer.popleft()
            # 从统计中减去
            if device_id in self.rolling_stats:
                self.rolling_stats[device_id]['wc_sum'] -= old_point.water_cut
                self.rolling_stats[device_id]['count'] -= 1

    def get_water_cut_rolling_avg(self, device_id: str) -> Optional[float]:
        """获取含水率24小时滚动平均值"""
        if device_id not in self.rolling_stats:
            return None

        stats = self.rolling_stats[device_id]
        if stats['count'] == 0:
            return None

        return stats['wc_sum'] / stats['count']

    def calculate_data_loss_rate(self, device_id: str, hours: int = 24) -> float:
        """计算数据丢失率"""
        if device_id not in self.data_buffer:
            return 1.0  # 100%丢失

        expected_points = hours * 60  # 每分钟一个点
        actual_points = len(self.data_buffer[device_id])

        if expected_points == 0:
            return 0.0

        loss_rate = 1 - (actual_points / expected_points)
        return max(0.0, min(1.0, loss_rate))

    def detect_duplicate_data(self, device_id: str, new_point: WellDataPoint) -> bool:
        """检测重复数据"""
        if device_id not in self.data_buffer:
            return False

        # 检查最近数据中是否有重复
        for point in list(self.data_buffer[device_id])[-10:]:  # 检查最近10个点
            if (abs(point.timestamp - new_point.timestamp).total_seconds() < 1 and
                    abs(point.pressure_psi - new_point.pressure_psi) < 0.1 and
                    abs(point.water_cut - new_point.water_cut) < 0.001):
                return True

        return False

    def check_temperature_flatline(self, device_id: str, duration_minutes: int = 10) -> bool:
        """检查温度平线"""
        if device_id not in self.data_buffer:
            return False

        buffer = list(self.data_buffer[device_id])
        if len(buffer) < duration_minutes:
            return False

        # 检查最近duration_minutes分钟的温度变化
        recent_temps = [point.temperature for point in buffer[-duration_minutes:]]
        if len(recent_temps) < 2:
            return False

        # 计算温度标准差
        temp_std = statistics.stdev(recent_temps) if len(recent_temps) > 1 else 0

        # 如果标准差非常小，说明温度平线
        return temp_std < 0.1  # 温度变化小于0.1度

    def get_historical_data(self, device_id: str,
                            start_time: datetime,
                            end_time: datetime) -> List[WellDataPoint]:
        """获取历史数据"""
        if device_id not in self.data_buffer:
            return []

        return [point for point in self.data_buffer[device_id]
                if start_time <= point.timestamp <= end_time]