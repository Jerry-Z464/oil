from pymodbus.client.sync import ModbusSerialClient

relay_inout = ModbusSerialClient(method='rtu',
                                 port='/dev/ttyCOM5',
                                 baudrate=9600,
                                 timeout=1,
                                 parity='N',
                                 stopbits=1,
                                 bytesize=8)
flag = relay_inout.connect()
if flag:
    print("successful connect to 485 relay")

# 方法1：直接读取40001（地址偏移为0）
result = client.read_holding_registers(0, count=1, unit=1)

if not result.isError():
    data = result.registers[0]
    print(data)
