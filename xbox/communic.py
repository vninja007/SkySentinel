from xbox_read import XboxController
import time
import serial

xc = XboxController()
#while True:
#    print(xc.read())

ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=115200,
    timeout=2)

ser.flush()

while True:
    print(xc.read())
    ser.write((str(xc.read()).replace(" ","")+"\n").encode('utf-8'))
    time.sleep(0.2)
    print(ser.readline())