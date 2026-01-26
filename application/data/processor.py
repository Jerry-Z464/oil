import time
from datetime import datetime
from application import app, logger, db
from application.entity import WellData
# from application.data.models import DataPoint


def process_data(measurements):
    try:
        with app.app_context():
            # 数据库健康检查
            # 存储设备数据
            well_data = WellData(code=measurements["wellCode"], dp=measurements["dp"], gvf=measurements["GVF"],
                                 gas_flow_rate=measurements["gasFlowRate"],
                                 liquid_flow_rate=measurements["liquidFlowRate"],
                                 oil_flow_rate=measurements["oilFlowRate"],
                                 pressure=measurements["pressure"],
                                 temperature=measurements["temperature"],
                                 water_cut=measurements["waterCut"],
                                 water_flow_rate=measurements["waterFlowRate"])
            db.session.add(well_data)
            db.session.commit()

            # point = DataPoint(device_id=str(measurements["wellCode"]),
            #                   timestamp=datetime.now(),
            #                   dp=measurements["dp"],
            #                   pressure=measurements["pressure"],
            #                   temperature=measurements["temperature"],
            #                   water_cut=measurements["waterCut"],
            #                   liquid_flow= measurements["liquidFlowRate"],
            #                   water_flow=measurements["waterFlowRate"],
            #                   oil_flow=measurements["oilFlowRate"],
            #                   gas_flow=measurements["gasFlowRate"])

            # data_analyzer.add_data(measurements["wellCode"], point)

    except Exception as e:
        logger.error("采集数据失败：{}".format(str(e)))
