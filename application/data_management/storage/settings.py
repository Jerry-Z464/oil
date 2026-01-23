import json
from typing import Any

from application.data_management.storage.database import Database
from application.data_management.storage.db_models import Setting


class SettingManager:
    """配置管理器"""

    def __init__(self, db: Database):
        self.db = db
        self._cache = {}

    def get(self, key: str) -> Any:
        """获取配置值"""

        # 先查缓存
        if key in self._cache:
            return self._cache[key]
        session = self.db.get_session()

        try:
            setting = session.query(Setting).filter_by(key=key).first()

            if setting is None:
                return None

            value = self._parse_value(setting.value)

            # 存入缓存
            self._cache[key] = value
            return value

        finally:
            session.close()

    def _parse_value(self, value: str) -> Any:
        """解析值"""
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    def refresh(self):
        """刷新缓存"""
        self._cache.clear()
