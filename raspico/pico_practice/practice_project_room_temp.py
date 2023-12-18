from lcd1602 import LCD
import machine
import utime
import math

thermistor = machine.ADC(28)
lcd = LCD()

try:
    while True:
        temperature_value = thermistor.read_u16()
        Vr = 3.3 * float(temperature_value) / 65535
        Rt = 10000 * Vr / (3.3 - Vr)
        #temp = 1/(((math.log(Rt / 10000)) / 3950 ) + (1 / (273.15+25)))
        temp = (298.15 * 3950)/(298.15 * math.log(Rt/10000) + 3950)
        Cel = temp - 273.15
#         Fah = Cel * 1.8 + 32
#         print(f"Celsius: {Cel:.2f} C Fahrenheit: {Fah:.2f} F")
#         utime.sleep_ms(200)

        string = f" Temperature is \n    {Cel:.2f} C"
        lcd.message(string)
        utime.sleep(1)
        lcd.clear()
except KeyboardInterrupt:
    lcd.clear()
    print("Exiting...")