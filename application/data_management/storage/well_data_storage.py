from application.data_management.models.well_data import WellData
from application.data_management.storage.database import Database
from application.data_management.storage.db_models import DeviceData


class WellDataStorage:

    def __init__(self, db: Database):
        self.db = db

    def save(self, device_id: str, well_data: WellData) -> bool:
        """
        保存数据

        返回:  True=成功, False=失败
        """
        session = self.db.get_session()

        try:
            data = DeviceData(
                device_id=device_id,
                cmt5_time=well_data.cmt5_time,
                dP=well_data.dP,
                gVF=well_data.gVF,
                gasFlowRate=well_data.gasFlowRate,
                liquidFlowRate=well_data.liquidFlowRate,
                oilFlowRate=well_data.oilFlowRate,
                pressure=well_data.pressure,
                temperature=well_data.temperature,
                waterCut=well_data.waterCut,
                waterFlowRate=well_data.waterFlowRate,
            )
            session.add(data)
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            print(f"[数据存储] 保存失败: {e}")
            return False
        finally:
            session.close()