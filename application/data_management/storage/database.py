from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from application.data_management.storage.db_models import Base


class Database:
    """数据库管理类"""

    def __init__(self, url: str):
        """
        初始化
        """
        self.engine = create_engine(url, echo=False)
        self._session_factory = sessionmaker(bind=self.engine)

    def create_tables(self):
        """创建所有表"""
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """获取 Session"""
        return self._session_factory()