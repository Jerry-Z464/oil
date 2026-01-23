import time
from typing import Optional

from sqlalchemy import func

from application.data_management.models.well_data import WellData
from application.data_management.storage.database import Database
from application.data_management.storage.db_models import DeviceData


class MeteringOptimizer:
    """计量优化器"""

    def __init__(self, device_id: str, db: Database):
        self.device_id = device_id
        self.db = db

        self._enabled = False  # 默认关闭
        self._correction_value: Optional[float] = None  # 修正值

    def enable(self):
        """开启优化器"""
        self._enabled = True

    def disable(self):
        """关闭优化器"""
        self._enabled = False
        self._correction_value = None  # 关闭时清除修正值

    def is_enabled(self) -> bool:
        """是否开启"""
        return self._enabled

    def process(self, well_data: WellData) -> WellData:
        """
        优化处理数据

        参数:
            well_data: 原始数据

        返回: 
            优化后的数据
        """

        if not self._enabled:
            return well_data

        # 如果已有修正值，直接应用
        if self._correction_value is not None:
            well_data.waterCut = self._apply_correction(well_data.waterCut)
            return well_data

        # 计算24小时平均值
        avg_water_cut = self._get_24h_avg_water_cut()

        # 无历史数据，不修正
        if avg_water_cut is None:
            return well_data

        # 计算差值
        diff = well_data.waterCut - avg_water_cut

        # 差值大于2%，记录修正值
        if abs(diff) > 2.0:
            self._correction_value = diff
            well_data.waterCut = self._apply_correction(well_data.waterCut)

        return well_data

    def _apply_correction(self, water_cut: float) -> float:
        """应用修正值"""
        corrected = water_cut - self._correction_value

        return corrected

    def _get_24h_avg_water_cut(self) -> Optional[float]:
        """获取24小时平均含水率"""

        session = self.db.get_session()

        try:
            now = int(time.time())
            hours_24_ago = now - 24 * 60 * 60

            result = session.query(func.avg(DeviceData.waterCut)).filter(
                DeviceData.device_id == self.device_id,
                DeviceData.cmt5_time >= hours_24_ago,
                DeviceData.cmt5_time <= now
            ).scalar()

            return result

        except Exception as e:
            print(f"[优化器] 查询平均值失败: {e}")
            return None
        finally:
            session.close()

    def reset_correction(self):
        """重置修正值（重新计算）"""
        self._correction_value = None

    def get_correction_value(self) -> Optional[float]:
        """获取当前修正值"""
        return self._correction_value
