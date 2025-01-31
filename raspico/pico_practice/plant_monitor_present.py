import urequests
import machine
import time

# Connect to the internet and set up webhook with ifttt
from secrets import *
from do_connect import *
do_connect()

event = 'water_low'
# Values can be passed to the webhook using x-www-form-urlencoded data:
# https://maker.ifttt.com/trigger/{event}/with/key/{webhooks_key}?value1=value1&value2=value2&value3=value3
# More examples at https://help.ifttt.com/hc/en-us/articles/115010230347
message=f"https://maker.ifttt.com/trigger/{event}/with/key/{secrets['webhooks_key']}"
