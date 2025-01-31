import board
import pwmio
import time
import random

    
class Group():
    # Implement LED groups as their objects
    max_brightness = 65534          # Max brightness for PWM
    default_brightness = 16383      # about 1/4 brightness for PWM
    group_counter = 0               # How many groups have been initiated, increments when group added
    
    def __init__(self, pin):
        # ID for each group for management purposes, based on number of groups
        self.id = Group.group_counter
        Group.group_counter += 1
        
        self.counter = random.randint(60, 60 * len(GPIO_pins)) # The availability counter, random b/w 50 and 80
        self.led = pwmio.PWMOut(pin, frequency = 1000)      # The PWM object for the given GPIO pin
        self.led.duty_cycle = self.default_brightness
        self.ready = False # Group is/isn't ready to flash
        
        
    def flash(self):
        self.led.duty_cycle = Group.max_brightness                      # Set the led to max to simulate first lightning strike
        intermit_bright = random.randint(Group.default_brightness, 24754)      # Set the brightness for in between primary strike and secondary
        
        # fade from max to in-between brightness
        print("primary flash")
        for brightness in range(Group.max_brightness, intermit_bright, -1):
            self.led.duty_cycle = brightness
        time.sleep(random.uniform(0.2, 0.5)) # Wait for a little bit in between primary and secondary flashes
        
        flashes = random.randint(1,3) # Have between 0 and 2 secondary flashes
        secondary_brightness = random.randint(int(Group.max_brightness * 0.635), int(Group.max_brightness * 0.875)) # The first flash's brightness will be random
        for flash in range(flashes):
            self.led.duty_cycle = secondary_brightness
            print("Secondary flash")
            
            # fade from initial brightness to a bit more than the default brightness, randomized
            for brightness in range(secondary_brightness, random.randint(int(Group.max_brightness * 0.375), int(Group.max_brightness * 0.5)), -1):
                self.led.duty_cycle = brightness
            # sleep for a small time between flashes
            time.sleep(random.uniform(0.2, 0.4))
            
            # decrease initial brightness slightly
            secondary_brightness = secondary_brightness - int(secondary_brightness / 20)
            
        # After flashes are over, reset counter and ready
        self.counter = random.randint(60, 60 * len(GPIO_pins))
        self.ready = False
            
    def group_info(self):
        if self.ready == True:
            print(f'Group {self.id} is ready, counter = {self.counter}')
        else:
            print(f'Group {self.id} is not ready, counter = {self.counter}')

#Initialize variables
GPIO_pins = [board.GP14, board.GP16, board.GP17]
available_groups = []

for pin in GPIO_pins:
    available_groups.append(Group(pin))

# State loop
while True:
    # If a group is ready, set it to ready
    # Otherwise, decrement its counter
    for group in available_groups:
        if group.counter <= 0:
            group.ready = True
        else:
            group.counter = group.counter - random.randint(1,len(GPIO_pins))
        group.group_info()
    
    # Debug, print each group and its counter
    #for group in available_groups:
    #    group.group_info()
    
    group = available_groups[random.randint(0,len(available_groups)-1)]
    if group.ready:
        print(f'Group {group.id} flashing')
        group.flash()
        
    time.sleep(1)
    
    
    
    
    
    