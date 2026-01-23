from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
import statistics
import logging
from collections import deque

from config import Config
from models.data_models import WellDataPoint, WaterCutSample, OptimizerState
from services.data_analyzer import DataAnalyzer

logger = logging.getLogger(__name__)


class WaterCutOptimizer:
    """含水率优化器"""

    def __init__(self, config: Config):
        self.config = config
        self.analyzer = DataAnalyzer(config)
        self.optimizer_states = {}  # device_id: OptimizerState
        self.wc_samples = defaultdict(list)  # device_id: List[WaterCutSample]
        self.comparison_points = defaultdict(deque)  # device_id: deque of deviations

    def enable_optimizer(self, device_id: str):
        """启用优化器"""
        if device_id not in self.optimizer_states:
            self.optimizer_states[device_id] = OptimizerState()

        self.optimizer_states[device_id].enabled = True
        self.optimizer_states[device_id].disabled_reason = None
        logger.info(f"Optimizer enabled for device {device_id}")

    def disable_optimizer(self, device_id: str, reason: str = "Manual"):
        """禁用优化器"""
        if device_id in self.optimizer_states:
            self.optimizer_states[device_id].enabled = False
            self.optimizer_states[device_id].disabled_reason = reason
            logger.info(f"Optimizer disabled for device {device_id}: {reason}")

    def add_water_cut_sample(self, device_id: str, wc_sample_avg: float) -> Optional[WaterCutSample]:
        """添加含水率样本"""
        # 获取当前滚动平均值
        wc_rolling_avg = self.analyzer.get_water_cut_rolling_avg(device_id)
        if wc_rolling_avg is None:
            logger.warning(f"No rolling average available for device {device_id}")
            return None

        # 计算偏差
        deviation_x = wc_sample_avg - wc_rolling_avg

        # 创建样本记录
        sample = WaterCutSample(
            timestamp=datetime.now(),
            device_id=device_id,
            wc_sample_avg=wc_sample_avg,
            wc_rolling_avg=wc_rolling_avg,
            deviation_x=deviation_x
        )

        # 存储样本
        self.wc_samples[device_id].append(sample)
        self.comparison_points[device_id].append(deviation_x)

        # 保持最多5个比较点
        if len(self.comparison_points[device_id]) > self.config.COMPARISON_POINTS:
            self.comparison_points[device_id].popleft()

        logger.info(f"WC sample added for device {device_id}: "
                    f"sample={wc_sample_avg:.3f}, rolling={wc_rolling_avg:.3f}, "
                    f"deviation={deviation_x:.3f}")

        # 检查是否需要启用优化器
        self._check_optimizer_condition(device_id)

        return sample

    def _check_optimizer_condition(self, device_id: str):
        """检查优化器启用条件"""
        if device_id not in self.comparison_points:
            return

        deviations = list(self.comparison_points[device_id])
        if len(deviations) < self.config.COMPARISON_POINTS:
            return

        # 计算平均绝对偏差
        avg_abs_deviation = statistics.mean(abs(d) for d in deviations)

        # 检查偏差超过阈值的比例
        significant_deviations = sum(1 for d in deviations if abs(d) > self.config.WC_DEVIATION_THRESHOLD)
        significant_ratio = significant_deviations / len(deviations)

        logger.debug(f"Device {device_id}: avg_abs_dev={avg_abs_deviation:.4f}, "
                     f"sig_ratio={significant_ratio:.2f}")

        if significant_ratio > 0.5:  # 超过50%的点偏差>2%
            # 计算平均偏差
            avg_deviation = statistics.mean(deviations)

            # 启用优化器
            if device_id not in self.optimizer_states:
                self.optimizer_states[device_id] = OptimizerState()

            self.optimizer_states[device_id].bias_x = avg_deviation
            self.optimizer_states[device_id].activation_time = datetime.now() + timedelta(minutes=1)
            self.enable_optimizer(device_id)

            logger.info(f"Optimizer activated for device {device_id} with bias {avg_deviation:.4f}")

    def check_auto_disable_conditions(self, device_id: str, data_point: WellDataPoint) -> bool:
        """检查自动禁用条件"""
        # 条件1: DP = 0 for >12h
        if data_point.dp_kpa == 0:
            # 这里需要检查连续12小时DP为0的逻辑
            # 简化实现：如果当前DP为0，检查优化器状态
            state = self.optimizer_states.get(device_id)
            if state and state.enabled:
                # 在实际实现中需要记录DP为0的开始时间
                # 这里简化处理
                pass

        # 条件2: Any abnormal alert
        # 这个在monitor中处理

        return False

    def apply_correction(self, device_id: str, water_cut_meas: float) -> float:
        """应用偏差修正"""
        if device_id not in self.optimizer_states:
            return water_cut_meas

        state = self.optimizer_states[device_id]

        if not state.enabled:
            return water_cut_meas

        # 检查是否到达激活时间
        if state.activation_time and datetime.now() < state.activation_time:
            return water_cut_meas

        # 应用修正
        corrected_wc = water_cut_meas + state.bias_x

        # 限制在0-100%
        corrected_wc = max(0.0, min(1.0, corrected_wc))

        return corrected_wc

    def calculate_flows(self, device_id: str, liquid_flow: float,
                        water_cut: float) -> Tuple[float, float]:
        """计算油水流量"""
        # 应用修正（如果需要）
        corrected_wc = self.apply_correction(device_id, water_cut)

        # 计算油水流量
        oil_flow = liquid_flow * (1 - corrected_wc)
        water_flow = liquid_flow * corrected_wc

        return oil_flow, water_flow

    def get_optimizer_status(self, device_id: str) -> Optional[Dict[str, Any]]:
        """获取优化器状态"""
        if device_id not in self.optimizer_states:
            return None

        state = self.optimizer_states[device_id]

        return {
            'enabled': state.enabled,
            'bias_x': state.bias_x,
            'activation_time': state.activation_time,
            'disabled_reason': state.disabled_reason,
            'last_sample_time': state.last_sample_time
        }