from machine import Pin, ADC
from machine import UART

class PlantMonitor:
    """Micropython class for MonkMakes capacitative plant monitor"""
    
    wetness = 0
    temp = 0
    humidity = 0
    
    uart = None
    led_on = True
    
    analog = ADC(28)
    
    def __init__(self):
        try:
            self.uart = UART(0, baudrate=9600, timeout=400, tx = Pin(0), rx = Pin(1))
        except:
            raise Exception("Unable to connect to monitor. Check the wiring.")
        
        # Getter Functions
        # Through UART, send a request character and receive the requested value
    def get_wetness(self):
        return float(self.request_property("w"))
    def get_temp(self):
        return float(self.request_property("t"))
    def get_humidity(self):
        return float(self.request_property("h"))
    
    # Control onboard LED
    def led_off(self):
        self.uart.write("l")
    def led_on(self):
        self.uart.write("L")
        
    def deinit(self):
        self.uart.deinit()
        
    # requests the property using the relevant character command
    # Wetness: "w"
    # Humidity: "h"
    # Temperature: "t"
    # Turn LED on: "L"
    # Turn LED off: "l"
    def request_property(self, cmd):
        self.uart.write(cmd)
        line = self.uart.readline()
        if line is not None and len(line) > 3:
            value_str = line[2:-2].decode()
            return value_str
        else:
            print("Communication error with monitor. Check the wiring.")
            return 0
