import network
import time
from secrets import *

# status				Value	Description
# STAT_IDLE				0		No connection and no activity
# STAT_CONNECTING		1		Connecting in progress
# STAT_WRONG_PASSWORD	-3		Failed due to incorrect password
# STAT_NO_AP_FOUND		-2		Failed because no access point replied
# STAT_CONNECT_FAIL		-1		Failed due to other problems
# STAT_GOT_IP			3		Connection Successful

def do_connect(ssid=secrets['ssid'], password=secrets['password'], lcd=None, retries=10, verbose=False):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # disables power save mode
    wlan.connect(secrets['ssid'], secrets['password'])

    # Wait for connect or fail
    while retries > 0 or wlan.status() == 2:
        if wlan.status() < 0 or wlan.status() >=3:
            break
        retries -=1
        if lcd != None:
            lcd.clear()
            lcd.message(f"  Connecting...\n    Status: {wlan.status()}")
        if verbose:
            print(f"Connecting to {ssid}, status {wlan.status()}...")
            
        time.sleep(1)
        
    # Handle connection error
    if wlan.status() != 3:
        if lcd != None:
            lcd.clear()
            lcd.message("Wifi connection\n     Failed")
        raise RuntimeError(f"Wifi connection failed, status {wlan.status()}")
    else:
        print("Connected")
        ip = wlan.ifconfig()[0]
        if lcd != None:
            lcd.clear()
            lcd.message(f"   Connected!\n{ip}")
            time.sleep(1)
            lcd.clear()
        print(f"Network Config: {ip}")
        return ip
    
# Returns true if Pi is connected to network
def is_connected():
    return wlan.status() == network.STAT_GOT_IP
