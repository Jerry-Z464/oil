import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
# import pandas as pd
import struct

# 修正后的完整测量点配置（根据文档1重新整理）
MEASUREMENT_POINTS = [
    {"name": "wellCode", "address": 40001, "unit": "", "type": "int", "rw": "rw", "description": "0 Start Testing  1 Stop Testing  2 Stop purging 3 Abort"},
    {"name": "command", "address": 40002, "unit": "", "type": "int", "rw": "ro", "description": "Start testing immediately if 0 is input"},
    {"name": "tempUnitSetting", "address": 40008, "unit": "", "type": "int", "rw": "rw", "description": "1: Celsius 2: Fahrenheit, Default: “1”"},
    {"name": "pressureUnitSetting", "address": 40009, "unit": "", "type": "int", "rw": "rw", "description": "1: Kpa, 2: Mpa, 3: bar, 4: inHg, 5: inH2O, 6: Psi, default: “1”"},
    {"name": "fluidRateUnitSetting", "address": 40010, "unit": "", "type": "int", "rw": "rw", "description": "1: m3/day, 2: ft3/d, 3: bbl/d, default: “1”"},
    {"name": "gasRateUnitSetting", "address": 40011, "unit": "", "type": "int", "rw": "rw", "description": "1: m3/day, 2: ft3/d, 3: MSCFD, 4: MMSCFD, default: “1”"},
    {"name": "liquidFlowRate", "address": 40028, "unit": "M³", "type": "float", "rw": "ro", "description": "Liquid Flow Rate"},
    {"name": "waterFlowRate", "address": 40030, "unit": "M³", "type": "float", "rw": "ro", "description": "Water Flow Rate"},
    {"name": "oilFlowRate", "address": 40032, "unit": "M³", "type": "float", "rw": "ro", "description": "Oil Flow Rate"},
    {"name": "gasFlowRate", "address": 40034, "unit": "M³", "type": "float", "rw": "ro", "description": "Gas Flow Rate"},
    {"name": "GVF", "address": 40036, "unit": "%", "type": "float", "rw": "ro", "description": "Gas Volume Fraction"},
    {"name": "temperature", "address": 40038, "unit": "℃", "type": "float", "rw": "ro", "description": "Temperature"},
    {"name": "pressure", "address": 40040, "unit": "kPa", "type": "float", "rw": "ro", "description": "Pressure"},
    {"name": "waterCut", "address": 40042, "unit": "%", "type": "float", "rw": "ro", "description": "Water Cut"}
]


def read_modbus_registers(client):
    """增强型寄存器读取函数"""
    data = {}
    for point in MEASUREMENT_POINTS:
        try:
            address = point["address"]
            reg_type = point["type"]

            if reg_type == "int":
                # 优化：支持批量读取INT类型
                result = client.read_holding_registers(
                    address=address,
                    count=1,
                    unit=1  # 从站地址需根据实际设备配置
                )
                data[point["name"]] = result.registers[0]

            elif reg_type == "float":
                # 优化：支持连续寄存器读取
                result = client.read_holding_registers(
                    address=address,
                    count=2,
                    unit=1
                )
                # 根据设备字节序调整解包方式
                float_val = struct.unpack('<f', struct.pack('HH', *result.registers))[0]
                data[point["name"]] = round(float_val, 2)

        except Exception as e:
            print(f"Error reading {point['name']} (Addr:{address}): {str(e)}")
    return data


def main():
    # 设备配置（根据实际情况修改）
    client = ModbusClient(
        method='rtu',
        port='/dev/ttyCOM5',  # Windows系统使用'COM1'
        baudrate=9600,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=2
    )

    if not client.connect():
        raise ConnectionError("Modbus connection failed")

    try:
        #df = pd.DataFrame(columns=[point["name"] for point in MEASUREMENT_POINTS])
        #timestamps = []

        while True:
            measurements = read_modbus_registers(client)
            print(data)
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
