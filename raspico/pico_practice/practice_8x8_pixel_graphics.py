import machine
import time

sdi = machine.Pin(18,machine.Pin.OUT)
rclk = machine.Pin(19,machine.Pin.OUT)
srclk = machine.Pin(20,machine.Pin.OUT)


glyph = [0xFF,0xEF,0xC7,0xAB,0xEF,0xEF,0xEF,0xFF]

# Shift the data to 74HC595
def hc595_in(dat):
    for bit in range(7,-1, -1):
        srclk.low()
        time.sleep_us(30)
        sdi.value(1 & (dat >> bit))
        time.sleep_us(30)
        srclk.high()

def hc595_out():
    rclk.high()
    time.sleep_us(200)
    rclk.low()
try:
    while True:
        for i in range(0,8):
            hc595_in(glyph[i])
            hc595_in(0x80>>i)
            hc595_out()
except:
    for i in range(18,21):
        machine.Pin(i,machine.Pin.OUT).value(0)