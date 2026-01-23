from typing import Dict

from application.data_management.modules.optimizer.metering_optimizer import MeteringOptimizer
from application.data_management.storage.database import Database


class OptimizerManager:

    def __init__(self, db: Database):
        self.db = db
        self._optimizers: Dict[str, MeteringOptimizer] = {}

    def get(self, device_id: str) -> MeteringOptimizer:

        if device_id not in self._optimizers:
            self._optimizers[device_id] = MeteringOptimizer(device_id, self.db)

        return self._optimizers[device_id]

    def enable(self, device_id: str):
        self. get(device_id).enable()

    def disable(self, device_id: str):
        self. get(device_id).disable()

    def enable_all(self):
        for optimizer in self._optimizers.values():
            optimizer.enable()

    def disable_all(self):
        for optimizer in self._optimizers.values():
            optimizer.disable()

    def clear(self):
        self._optimizers.clear()