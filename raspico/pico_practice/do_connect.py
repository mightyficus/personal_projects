import network
import time
from secrets import *

# status				Value	Description
# STAT_IDLE				0		No connection and no activity
# STAT_CONNECTING		1		Connecting in progress
# STAT_WRONG_PASSWORD	-3		Failed due to incorrect password
# STAT_NO_AP_FOUND		-2		Failed because no access point replied
# STAT_CONNECT_FAIL		-1		Failed due to other problems
# STAT_GOT_OP			3		Connection Successful

def do_connect(ssid=secrets['ssid'], password=secrets['password']):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets['ssid'], secrets['password'])

    # Wait for connect or fail
    wait = 10
    while wait > 0:
        if wlan.status() < 0 or wlan.status() >=3:
            break
        wait -=1
        print(f"Waiting for connection, status {wlan.status()}...")
        time.sleep(1)
        
    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError(f"Wifi connection failed, status {wlan.status()}")
    else:
        print("Connected")
        ip = wlan.ifconfig()[0]
        print(f"Network Config: {ip}")
        return ip
