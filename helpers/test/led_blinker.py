from gpiozero import LED
from time import sleep

led = LED(17)
delay = .1

while True:
    led.on()
    sleep(delay)
    led.off()
    sleep(delay)