import SerialComm

ser = SerialComm.SerialComm(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
print ser.login_status()
ser.login('root', 'zilogic')
print ser.login_status()
