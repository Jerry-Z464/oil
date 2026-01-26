import time
import struct
import threading
from application import app, logger, modbus_client
from application.data.processor import process_data

MEASUREMENT_POINTS = [
    {"name": "wellCode", "address": 0, "unit": "", "type": "int", "decimla": 0, "description": "0 Start Testing  1 Stop Testing  2 Stop purging 3 Abort"},
    # {"name": "command", "address": 1, "unit": "", "type": "int", "decimla": 0, "description": "Start testing immediately if 0 is input"},
    # {"name": "tempUnitSetting", "address": 7, "unit": "", "type": "int", "decimla": 0, "description": "1: Celsius 2: Fahrenheit, Default: “1”"},
    # {"name": "pressureUnitSetting", "address": 8, "unit": "", "type": "int", "decimla": 0, "description": "1: Kpa, 2: Mpa, 3: bar, 4: inHg, 5: inH2O, 6: Psi, default: “1”"},
    # {"name": "fluidRateUnitSetting", "address": 9, "unit": "", "type": "int", "decimla": 0, "description": "1: m3/day, 2: ft3/d, 3: bbl/d, default: “1”"},
    # {"name": "gasRateUnitSetting", "address": 10, "unit": "", "type": "int", "decimla": 0, "description": "1: m3/day, 2: ft3/d, 3: MSCFD, 4: MMSCFD, default: “1”"},
    {"name": "liquidFlowRate", "address": 27, "unit": "M³", "type": "float", "decimla": 2, "description": "Liquid Flow Rate"},
    {"name": "waterFlowRate", "address": 29, "unit": "M³", "type": "float", "decimla": 2, "description": "Water Flow Rate"},
    {"name": "oilFlowRate", "address": 31, "unit": "M³", "type": "float", "decimla": 2, "description": "Oil Flow Rate"},
    {"name": "gasFlowRate", "address": 33, "unit": "M³", "type": "float", "decimla": 2, "description": "Gas Flow Rate"},
    {"name": "GVF", "address": 35, "unit": "%", "type": "float", "decimla": 2, "description": "Gas Volume Fraction"},
    {"name": "temperature", "address": 37, "unit": "℃", "type": "float", "decimla": 2, "description": "Temperature"},
    {"name": "pressure", "address": 39, "unit": "kPa", "type": "float", "decimla": 2, "description": "Pressure"},
    {"name": "waterCut", "address": 41, "unit": "%", "type": "float", "decimla": 2, "description": "Water Cut"},
    {"name": "dp", "address": 100, "unit": "", "type": "float", "decimla": 2, "description": "Differential Pressure"}
]


def read_modbus_registers():
    data = {}
    for point in MEASUREMENT_POINTS:
        address = point["address"]
        reg_type = point["type"]
        try:
            if reg_type == "int":
                result = modbus_client.read_holding_registers(
                    address=address,
                    count=1,
                    unit=1
                )
                data[point["name"]] = result.registers[0]
            elif reg_type == "float":
                result = modbus_client.read_holding_registers(
                    address=address,
                    count=2,
                    unit=1
                )
                # 大端解析
                byte_data = bytes()
                for reg in result.registers:
                    byte_data += reg.to_bytes(2, byteorder='big')
                # 解析为浮点数（>f 表示大端浮点数）
                float_value = struct.unpack('>f', byte_data)[0]
                data[point["name"]] = round(float_value, 2)
        except Exception as e:
            logger.error(f"Error reading {point['name']} (Addr:{address}): {str(e)}")
    return data


def read_data():
    """
    读取Modbus数据
    :return:
    """
    while True:
        try:
            measurements = read_modbus_registers()
            logger.info("采集数据：{}".format(measurements))
            threading.Thread(target=process_data, args=(measurements,), daemon=True).start()
            time.sleep(app.config["INTERVAL"])
        except Exception as e:
            logger.error("采集数据失败：{}".format(str(e)))
