
#200 steps/rev
#12V, 350mA
#1/8 microstep mode
#Turn a 200 step motor left one full revolution: 1600

from time import sleep
import RPi.GPIO as gpio #https://pypi.python.org/pypi/RPi.GPIO
#import exitHandler #uncomment this and line 58 if using exitHandler

class Stepper(object):
	#instantiate stepper 
	#pins = [stepPin, directionPin, enablePin]
	def __init__(self, pins, steps = 1600, default_cw = True):
		#setup pins
		self.pins = pins
		self.stepPin = self.pins[0]
		self.directionPin = self.pins[1]
		self.enablePin = self.pins[2]
		self.steps = steps
		self.default_cw = default_cw
		
		#use the broadcom layout for the gpio
		gpio.setmode(gpio.BCM)
		
		#set gpio pins
		gpio.setup(self.stepPin, gpio.OUT)
		gpio.setup(self.directionPin, gpio.OUT)
		gpio.setup(self.enablePin, gpio.OUT)
		
		#set enable to high (i.e. power is NOT going to the motor)
		gpio.output(self.enablePin, True)
		
		#print("Stepper initialized (step=" + str(self.stepPin) + ", direction=" + str(self.directionPin) + ", enable=" + str(self.enablePin + ")")
	
	#clears GPIO settings
	def cleanGPIO(self):
		gpio.cleanup()
	
	#step the motor
	# steps = number of steps to take
	# dir = direction stepper will move
	# speed = defines the denominator in the waitTime equation: waitTime = 0.000001/speed. As "speed" is increased, the waitTime between steps is lowered
	# stayOn = defines whether or not stepper should stay "on" or not. If stepper will need to receive a new step command immediately, this should be set to "True." Otherwise, it should remain at "False."
	def rotate(self, degrees, dir, speed=1, stay_on=False, ease = False):
		#set enable to low (i.e. power IS going to the motor)
		steps = (degrees/360) * self.steps
		gpio.output(self.enablePin, False)
		
		#set the output to true for left and false for right
		cw = self.default_cw
		if (dir == "right" or dir == "cw"):
			cw =  not self.default_cw;
		elif (dir != "left" and dir != "acw"):
			print("STEPPER ERROR: no direction supplied")
			return False
		    
		gpio.output(self.directionPin, cw)

		sc = 0	
		wait_time = .0001/speed #waitTime controls speed		
		last_quarter = steps * 0.75
		quarter = steps - last_quarter
                
		while sc < steps:
                    wt = wait_time
                    
                    if ease and (sc > last_quarter):			
                        wt = wait_time * (1 + ((steps - sc)/quarter))  
                
                
                    #gracefully exit if ctr-c is pressed
                    #exitHandler.exitPoint(True) #exitHandler.exitPoint(True, cleanGPIO)

                    #turning the gpio on and off tells the easy driver to take one step
                    gpio.output(self.stepPin, True)
                    sleep(wt)
                    gpio.output(self.stepPin, False)
                    sleep(wt)
                    
                    sc += 1			
			
		gpio.output(self.directionPin, not cw)
		
		if (stay_on == False):
			#set enable to high (i.e. power is NOT going to the motor)
			gpio.output(self.enablePin, True)

		print("Stepper rotate complete (turned " + dir + " " + str(degrees) + " degrees)")
		