import logging

from application.data_management.models.well_data import WellData
from application.data_management.storage.database import Database
from application.data_management.storage.db_models import Device


class OnlineStatusMonitor:

    def __init__(self, db: Database):
        self.db = db

    def process(self, device_id: str, well_data: WellData):
        """
        处理在线状态监测
        """
        # 更新设备的最后更新时间
        logging.info(f'{device_id} 更新时间为 {well_data.cmt5_time}')
        with self.db.get_session() as session:
            session.query(Device).filter(Device.id == device_id).update({
                Device.last_update_time: well_data.cmt5_time
            })
            session.commit()
        return []