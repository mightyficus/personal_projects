import machine
import time

TRIG = machine.Pin(17, machine.Pin.OUT)
ECHO = machine.Pin(16, machine.Pin.IN)

def distance():
    # reset the pin that sends the ultrasonic pulse
    TRIG.low()
    time.sleep_us(2)
    # Transmit a 10 us ultrasonic pulse
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()
    # Make sure the ECHO pin isn't still receiving a value
    while not ECHO.value():
        pass
    # Set the start time
    time1 = time.ticks_us()
    # Wait until the ECHO pin receives a signal
    while ECHO.value():
        pass
    # Set the end time
    time2 = time.ticks_us()
    # Find how long it took between sending the pulse and receiving it
    duration = time.ticks_diff(time2,time1)
    print(f"Difference: {duration} us")
    # Find the time using the time difference and the speed of sound (340 m/s)
    # Dividing by 10,000 gives us the result in cm
    return duration * 340 / 2 / 10000

try:
    while True:
        dis = distance()
        print(f"Distance: {dis:.2f} cm")
        time.sleep_ms(300)
        
except KeyboardInterrupt:
    TRIG.value(0)
    ECHO.value(0)
    print("Exiting")
