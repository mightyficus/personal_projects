import urequests
import machine
import time
import pmon
from lcd1602 import LCD
from microdot import Microdot

# Connect to the internet and set up webhook with ifttt
from secrets import *
from do_connect import *
#do_connect(verbose=True)

# Name of IFTTT event
#event = 'water_low'
# Values can be passed to the webhook using x-www-form-urlencoded data:
# https://maker.ifttt.com/trigger/{event}/with/key/{webhooks_key}?value1=value1&value2=value2&value3=value3
# More examples at https://help.ifttt.com/hc/en-us/articles/115010230347
#message=f"https://maker.ifttt.com/trigger/{event}/with/key/{secrets['webhooks_key']}"



html_standard = """
<!DOCTYPE html>
<html>
    <head>
        <title>My Plant</title>
        <meta http-equiv="refresh" content="1" >
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <h1>Pico W Plant Monitor</h1>{warning}
        <h2 style='color: {color}' >Water: {water}%</h2>
        <h2>Temp: {temp:.2f} F</h2>
        <h2>Humidity: {humidity}%</h2>
    </body>
</html>
"""


try:
    lcd = LCD()
except:
    lcd = None
    print("LCD not Connected")
    
do_connect(verbose=True, lcd=lcd)
pm = pmon.PlantMonitor()
app = Microdot()

@app.route('/')
def index(request):
    # Get values from Sensor
    w = pm.get_wetness()
    t = pm.get_temp() * 1.8 + 32
    h = pm.get_humidity()
    color = ""
    warning = ""
    
    # If the soil is dry, print a warning
    if w < 15:
        color = "red"
        warning = "\n\t<h2 style='color: red;'>Your plant may be too dry!</h2>"
    else:
        color = "black"
        warning = ""
    
    
    # Display Wetness and temperature on LCD
    if lcd != None:
        lcd.clear()
        lcd.message(f"Wetness: {w}%\nTemp: {t:.2f} F")
    
    # Display all values on the command line
    print(f"Wetness: {w}%, Temperature: {t:.2f} F, Humidity: {h}%")
    
    response = html_standard.format(water=w, temp=t, humidity=h, color=color, warning=warning)
    return response, {'Content-Type': 'text/html'}
try:
    app.run(port=80, debug=True)
except KeyboardInterrupt:
    if lcd != None:
        lcd.clear()
    app.shutdown()