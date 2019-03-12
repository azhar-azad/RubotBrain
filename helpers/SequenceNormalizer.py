import os, sys
import numpy as np
import copy


class SequenceNormalizer(object): 
    def __init__(self):
        
        self.moves = ["F", "R", "B", "L", "U", "D", "F'", "R'", "B'", "L'", "U'", "D'", "F2", "R2", "B2", "L2", "U2", "D2"]
		
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
	
    def wcr(self, steppers, move):
        if move not in self.whole_cube_rotations.keys():
            raise ValueError("Not a valid move")
                

        for rs in self.whole_cube_rotations[move]:	
            first = steppers[rs[0]]
            for i in range(len(rs)-1):
                _to = rs[i]
                _from = rs[i+1]
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
    
   
if __name__ == "__main__":  pass
    
