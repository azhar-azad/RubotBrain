import os, sys
import RPi.GPIO as gpio
try:
    from .Stepper import Stepper
except (ImportError, SystemError):
    from Stepper import Stepper

from time import sleep
import numpy as np
import copy

#stepper variables
#[stepPin, directionPin, enablePin]

class StepperController(object): 
    def __init__(self):
        
        self.faces = ['F', 'R', 'B', 'L', 'U', 'D']
		
		self.slice_turns= {
			"M" : ("X'", ["R", "L'"]), 
			"M'": ("X",  ["R'", "L"]), 
			"M2": ("X2", ["R2", "L2"]), 
			"E" : ("Y'", ["U", "D'"]), 
			"E'": ("Y",  ["U'", "D"]), 
			"E2": ("Y2", ["U2", "D2"]), 
			"S" : ("Z",  ["F'", "B"]), 
			"S'": ("Z'", ["F", "B'"])
			"S2": ("Z2", ["F2", "B2"])
		}
		
		self.whole_cube_rotations = {
			"X" : [["F", "D", "B", "U"]], 
			"X'": [["F", "U", "B", "D"]],
			"X2": [["F", "B"], ["U", "D"]],
			"Y" : [["F", "R", "B", "L"]], 
			"Y'": [["F", "L", "B", "R"]], 
			"Y2": [["F", "B"], ["L", "R"]], 
			"Z" : [["U", "L", "D", "R"]]
			"Z'": [["U", "R", "D", "L"]], 
			"Z2": [["U", "D"], ["R", "L"]], 
		}

        self.steppers = {
            'F' : Stepper([20, 21, 16], default_cw = False), #4
            'R' : Stepper([ 7, 12,  8], default_cw = False), #6
            'B' : Stepper([23, 24, 25], default_cw = False), #5
            'L' : Stepper([19, 26, 13], default_cw = False), #3
            'U' : Stepper([17, 27,  3], default_cw = False), #1
            'D' : Stepper([ 5,  6, 22], default_cw = False)  #2  
            }
        

    def __del__(self): pass
		
	def rotate(self, face, degrees = 90, dir = "cw", speed = 1):
        if face not in self.faces:
            raise ValueError("Not a valid movement")
        
        self.steppers[face].rotate(degrees = degrees, dir = dir, speed = speed)
	
	def wcr(self, steppers, move):
		if move not in self.whole_cube_rotations.keys():
			raise ValueError("Not a valid move")
			
		rotseq = self.whole_cube_rotations[move]		
		first = steppers[rotseq[0]]
		
		for i in range(3):
			_to = rotseq[i]
			_from = rotseq[i+1]
			steppers[_to] = steppers[_from]
		
		steppers[3] = first
		
		
	def slice_turn(self, steppers, move, speed = 1, ease = False, interval = 0.5,): 
		if move not in self.slice_turns.keys():
			raise ValueError("Not a valid move")
			
		seq = self.slice_turns[move]
		wcr = seq[0]
		rot = seq[1]
		
		self.wcr(steppers, wcr)
		
		if len(rot) > 0:
			for r in rot:
				self.run(r, speed = speed, ease = ease, steppers = steppers)
				sleep(interval)
				
        
    def normalize_sequence(self, seq):
		nseq = seq.copy()
		return nseq
	
	def run(self, move, speed = 1, ease = False, steppers = self.steppers):
        degrees = 90
		dir = "cw"
        if len(move) > 1:
			if move[1] == '2':
                    degrees = 180
                else:
                    dir = "acw"
            
        face = move[0].upper()
        
        if face not in self.faces:
            raise ValueError("Not a valid movement")
        
        stepper = steppers[face]
        stepper.rotate(degrees = degrees, dir = dir, speed = speed)
                

    def run_sequence(self, seq, speed = 1, ease = False, interval = 0.5):
		_steppers = copy.deepcopy(self.steppers)

		for s in seq:
			
			if s in self.whole_cube_rotations.keys():
				self.wcr(_steppers, s)
				
			elif s in self.slice_turns.keys()
				self.slice_turn(_steppers, s, speed = speed, ease = ease, interval = interval)

			else:
				self.run(s, speed = speed, ease = ease, steppers = _steppers)
				sleep(interval)
		
	
	
    
    
    def test(self):
        interval = 0.1;
        stepper_speed = 1;
        
        sleep(1)
        #test stepper

        for t in range(3):
            for f in StepperController.faces:            
                StepperController.steppers[f].rotate(90, "cw", speed = stepper_speed)
                sleep(interval)
            
            sleep(1)
            
            for f in StepperController.faces:            
                StepperController.steppers[f].rotate(90, "acw", speed = stepper_speed)
                sleep(interval)
                        
            sleep(1)
            
if __name__ == "__main__":    
    sleep(3)
    sc = StepperController()
    #sc.run_sequence(["F", "R", "B", "L", "D", "U", "F'", "R'", "B'", "L'", "D'", "U'"], interval = 5, speed=.75)
    #for d in  [("F", "F'"), ("R", "R'"), ("B", "B'"), ("L", "L'"), ("D", "D'"), ("U", "U'")]:
    #    sc.run_sequence([d[0], d[0], d[1], d[1], d[1], d[1], d[0], d[0]], degrees = 90, interval = .5, speed=1)
    #   sleep(3)
    for i in range(2):
        sc.run_sequence(["F2", "R2", "B2", "L2", "D2", "U2", "F'", "R'", "B'", "L'", "D'", "U'"], interval = .5, speed= 1, ease = True)