from time import sleep
import RPi.GPIO as gpio
from collections import Counter

delay = .5
pins = [3, 25, 18]
c = len(pins)


gpio.setmode(gpio.BCM)
gpio.cleanup()
		
#set gpio pins
for pin in pins:
    gpio.setup(pin, gpio.OUT)

if c > 0:
    i = 0
    last_pin = pins[0]
    
    while True:
        gpio.output(last_pin, False)
        gpio.output(pins[i], True)
        last_pin = pins[i]
        i=i+1
        if i >= c:
            i = 0
        sleep(delay)
    
    
