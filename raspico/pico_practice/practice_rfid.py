from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=5,rst=0)

def write():
    to_write = input("Please enter the message: ")
    print("Writing... Please place card near reader...")
    id,text = reader.write(to_write)
    print(f"ID: {id}\nText: {text}")
    
def read():
    print("Reading... Please place card near reader...")
    id,text = reader.read()
    print(f"ID: {id}\nText: {text}")
    
read()