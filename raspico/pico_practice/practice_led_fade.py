import machine
import utime

led = machine.PWM(machine.Pin(15))
led.freq(1000)

for brightness in range(0,65535,50):
    led.duty_u16(brightness)
    utime.sleep_ms(5)
    print(brightness)
print("out of loop")
    
led.deinit()
machine.Pin(15, machine.Pin.OUT).value(0)