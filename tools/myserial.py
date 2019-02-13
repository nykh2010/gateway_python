import serial
import os
import time

ser = serial.Serial("/dev/ttyUSB0", 9600)

def read_port():
    while True:
        buf = ser.readline()
        if buf:
            print(buf)
            print(time.time())

def write_port():
    count = 10
    while count:
        count -= 1
        time.sleep(10)
        ser.write("hello\n".encode("utf-8"))
        ser.flush()
        print(time.time())
        
pid = os.fork()
if pid == 0:
    print("child process")
    read_port()
else:
    print("father process")
    write_port()
