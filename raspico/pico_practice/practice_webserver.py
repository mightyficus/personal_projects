import machine
import socket
import math
import time

from secrets import *
from do_connect import *

red = machine.Pin(13, machine.Pin.OUT)
green = machine.Pin(14, machine.Pin.OUT)
blue = machine.Pin(15, machine.Pin.OUT)

def webpage():
    html = """
    <!DOCTYPE html>
    <html>
    <body>
        <form action="./red">
            <input type="submit" value="Red " />
        </form>
        <form action="./green">
            <input type="submit" value="Green" />
        </form>
        <form action="./blue">
            <input type="submit" value="Blue" />
        </form>
        <form action="./off">
            <input type="submit" value="Off" />
        </form>
    </body>
    </html>
    """
    return html

def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        
        print(request)
        
        if request == '/off?':
            red.low()
            green.low()
            blue.low()
        elif request == '/red?':
            red.high()
            green.low()
            blue.low()
        elif request == '/green?':
            red.low()
            green.high()
            blue.low()
        elif request == '/blue?':
            red.low()
            green.low()
            blue.high()
            
        html = webpage()
        client.send(html)
        client.close()
        
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return(connection)


try:
    ip=do_connect()
    if ip is not None:
        connection = open_socket(ip)
        serve(connection)
except KeyboardInterrupt:
    #connection.shutdown(socket.SHUT_RDWR)
    connection.close()
    #print(connection)
    red.low()
    green.low()
    blue.low()
    print("exiting...")
    machine.reset()






