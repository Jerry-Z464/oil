from pymodbus.client.sync import ModbusSerialClient

relay_inout = ModbusSerialClient(method='rtu',
                                 port='/dev/ttyCOM5',
                                 baudrate=9600,
                                 timeout=1,
                                 parity='N',
                                 stopbits=1,
                                 bytesize=8)
result = relay_inout.connect()
if result:
    print("successful connect to 485 relay")
