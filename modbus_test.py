import time
import struct
from pymodbus.client.sync import ModbusSerialClient


MEASUREMENT_POINTS = [
    {"name": "wellCode", "address": 0, "unit": "", "type": "int", "decimla": 0, "description": "0 Start Testing  1 Stop Testing  2 Stop purging 3 Abort"},
    {"name": "command", "address": 1, "unit": "", "type": "int", "decimla": 0, "description": "Start testing immediately if 0 is input"},
    {"name": "tempUnitSetting", "address": 7, "unit": "", "type": "int", "decimla": 0, "description": "1: Celsius 2: Fahrenheit, Default: “1”"},
    {"name": "pressureUnitSetting", "address": 8, "unit": "", "type": "int", "decimla": 0, "description": "1: Kpa, 2: Mpa, 3: bar, 4: inHg, 5: inH2O, 6: Psi, default: “1”"},
    {"name": "fluidRateUnitSetting", "address": 9, "unit": "", "type": "int", "decimla": 0, "description": "1: m3/day, 2: ft3/d, 3: bbl/d, default: “1”"},
    {"name": "gasRateUnitSetting", "address": 10, "unit": "", "type": "int", "decimla": 0, "description": "1: m3/day, 2: ft3/d, 3: MSCFD, 4: MMSCFD, default: “1”"},
    {"name": "liquidFlowRate", "address": 27, "unit": "M³", "type": "float", "decimla": 2, "description": "Liquid Flow Rate"},
    {"name": "waterFlowRate", "address": 29, "unit": "M³", "type": "float", "decimla": 2, "description": "Water Flow Rate"},
    {"name": "oilFlowRate", "address": 31, "unit": "M³", "type": "float", "decimla": 2, "description": "Oil Flow Rate"},
    {"name": "gasFlowRate", "address": 33, "unit": "M³", "type": "float", "decimla": 2, "description": "Gas Flow Rate"},
    {"name": "GVF", "address": 35, "unit": "%", "type": "float", "decimla": 2, "description": "Gas Volume Fraction"},
    {"name": "temperature", "address": 37, "unit": "℃", "type": "float", "decimla": 2, "description": "Temperature"},
    {"name": "pressure", "address": 39, "unit": "kPa", "type": "float", "decimla": 2, "description": "Pressure"},
    {"name": "waterCut", "address": 41, "unit": "%", "type": "float", "decimla": 2, "description": "Water Cut"},
    {"name": "dP", "address": 100, "unit": "", "type": "float", "decimla": 2, "description": "dP"}
]


def read_modbus_registers(client):
    data = {}
    for point in MEASUREMENT_POINTS:
        try:
            address = point["address"]
            reg_type = point["type"]

            if reg_type == "int":
                result = client.read_holding_registers(
                    address=address,
                    count=1,
                    unit=1
                )
                data[point["name"]] = result.registers[0]
            elif reg_type == "float":
                # 优化：支持连续寄存器读取
                result = client.read_holding_registers(
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
            print(f"Error reading {point['name']} (Addr:{address}): {str(e)}")
    return data


def main():
    # 设备配置（根据实际情况修改）
    client = ModbusSerialClient(
        method='rtu',
        port='/dev/ttyCOM5',  # Windows系统使用'COM1'
        baudrate=9600,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=5
    )

    if not client.connect():
        raise ConnectionError("Modbus connection failed")

    try:

        #df = pd.DataFrame(columns=[point["name"] for point in MEASUREMENT_POINTS])
        #timestamps = []

        while True:
            measurements = read_modbus_registers(client)
            print(measurements)
            #measurements["Timestamp"] = pd.Timestamp.now()

            #df = df.append(measurements, ignore_index=True)
            #timestamps.append(pd.Timestamp.now())

            # 动态采样间隔（示例：压力每1秒，温度每5秒）
            #time.sleep(1 if any(p in measurements for p in ["pressure"]) else 5)
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nData collection stopped by user")
    finally:
        # 数据完整性校验
        #if not df.empty:
            #print(f"\nData integrity check: {len(df)} records collected")
            #df.to_csv("modbus_data.csv", index=False)
        client.close()


if __name__ == "__main__":
    main()
