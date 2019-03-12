from __future__ import print_function
from time import sleep
from helpers.RubiksScanner import RubiksScanner
from helpers.StepperController import StepperController
from rubik_solver.RubiksSolver import RubiksSolver
import RPi.GPIO as gpio

#steps
# 1. Scan the rubiks
# 2. Call the rubiks solver
# 3. Rotate steppers

gpio.setmode(gpio.BCM)
gpio.cleanup()

scanning_led_pin = -1
solving_led_pin = -1
error_led_pin = -1

if scanning_led_pin > 0:
    gpio.setup(scanning_led_pin, gpio.OUT)
if solving_led_pin > 0:
    gpio.setup(solving_led_pin, gpio.OUT)
if error_led_pin > 0:
    gpio.setup(error_led_pin, gpio.OUT)

solving_algorithms = ['Beginner', 'CFOP', 'Kociemba']  

rubiks_scanner = RubiksScanner()
stepper_controller = StepperController()
rubiks_solver = RubiksSolver()

sleep(1)

# Scan the Cube
if scanning_led_pin > 0:
    gpio.output(scanning_led_pin, True)
    
cube_string = rubiks_scanner.scan(speed = 3, interval = 1, debug = True)
#cube_string = "rrgwyywryybbwbwbobogboryowyrbrrggogowbgyogwowyrgyworbg"
rubiks_solver.print_cube(cube_string, color = False)

print(cube_string)

sleep(1)

if scanning_led_pin > 0:
    gpio.output(scanning_led_pin, False)
    
    
# Check validity
if rubiks_solver.is_valid_cube(cube_string):
    sleep(1)
    
    if solving_led_pin > 0:
        gpio.output(solving_led_pin, True)    
    
    solution = rubiks_solver.solve(cube = cube_string, method = solving_algorithms[2])
    solution = map(str, solution)
    print(solution)
    
    stepper_controller.run_sequence(solution, speed = 3, interval = 1)
    
    if solving_led_pin > 0:
        gpio.output(solving_led_pin, False)
    
else:
    print("Scanned cube is not valid")
    if error_led_pin > 0:
        gpio.output(error_led_pin, True)
    

sleep(10)
gpio.cleanup()
