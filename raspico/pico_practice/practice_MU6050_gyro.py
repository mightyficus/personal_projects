from imu import MPU6050
from machine import I2C, Pin
import time

i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
mpu = MPU6050(i2c)

try:
    while True:
        print(f"x: {mpu.accel.x}, y: {mpu.accel.y}, z: {mpu.accel.z}")
        time.sleep(0.1)
        print(f"A: {mpu.gyro.x}, B: {mpu.gyro.y}, Y: {mpu.gyro.z}")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")