# Reference: https://how2electronics.com/interfacing-dht11-temperature-humidity-sensor-with-raspberry-pi-pico/

# From DHT data sheet (https://www.mouser.com/datasheet/2/758/DHT11-Technical-Data-Sheet-Translated-Version-1143054.pdf): 
# Temperature range is 0 - 50 C +- 2
# Humidity range is 20 - 80% RH +- 5%

from machine import Pin, I2C
import utime as time
from dht import DHT11, InvalidPulseCount

pin = Pin(16, Pin.IN, Pin.PULL_UP)
sensor = DHT11(pin)
time.sleep(5)  # initial delay


pin = Pin(16, Pin.IN, Pin.PULL_UP)
sensor = DHT11(pin)
time.sleep(5)

try:
    while True:
        try:
            sensor.measure()
            print(f"Temperature:\t{sensor.temperature}")
            print(f"Humidity:\t{sensor.humidity}")
            time.sleep(4)
            
        except InvalidPulseCount as e:
            print("Bad pulse count - retrying...")
except KeyboardInterrupt:
    sensor = Pin(16).value(0)
    print("Exiting...")