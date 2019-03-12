from __future__ import print_function
import os, sys
from collections import OrderedDict
from picamera import PiCamera
from time import sleep
from PIL import Image, ImageDraw, ImageFont
import pickle

try:
    from .StepperController import StepperController
except (ImportError, SystemError):
    from StepperController import StepperController
    
try:
    from .ColorGuesser import ColorGuesser
except (ImportError, SystemError):
    from ColorGuesser import ColorGuesser


data_file = 'helpers/scan_regions.dat'

class RubiksScanner(object):   
    
    def __init__(self):
        self.key_regions = {}
        self.move_sequence = [
            ("R'" , [(1, 'U', 2), (2, 'U', 5), (3, 'U', 8), (4, 'R', 2), (5, 'R', 1), (6, 'R', 0)]), #scan 1
            ("R'" , [(1, 'B', 6), (2, 'B', 3), (3, 'B', 0), (4, 'R', 8), (5, 'R', 5)             ]), #scan 2
            ("R'" , [(1, 'D', 2), (2, 'D', 5), (3, 'D', 8), (4, 'R', 6), (5, 'R', 7)             ]), #scan 3
            ("R'" , [(1, 'F', 2), (2, 'F', 5), (3, 'F', 8),              (5, 'R', 3)             ]), #scan 4
            ("F"  , [(1, 'F', 0), (2, 'F', 1),              (4, 'U', 6), (5, 'U', 7)             ]), #scan 5
            ("F"  , [(1, 'F', 6), (2, 'F', 3),              (4, 'L', 8), (5, 'L', 5), (6, 'L', 2)]), #scan 6
            ("F"  , [             (2, 'F', 7),                           (5, 'D', 1), (6, 'D', 0)]), #scan 7
            ("F"  , [                                                                            ]),
            
            ("B'" , [                                                                            ]),
            ("B'" , [                                                                            ]),
            ("R'" , [(1, 'D', 6)                                                                 ]), #scan 8
            ("R'" , [(1, 'B', 2), (2, 'B', 5), (3, 'B', 8), (4, 'L', 0), (5, 'L', 3), (6, 'L', 6)]), #scan 9
            ("R'" , [                          (3, 'U', 0)                                       ]), #scan 10
            ("R'" , [                                                                            ]),
            ("B"  , [                                                                            ]),        
            ("R'" , [                                                                            ]),
            ("R'" , [             (2, 'B', 1),                           (5, 'U', 1)             ]), #scan 11
            ("R'" , [                                                                            ]), 
            ("R'" , [                                                                            ]), 
            ("B"  , [                                                                            ]), 
            ("B"  , [                                                                            ]), 
            ("R'" , [                                                                            ]),
            ("R'" , [             (2, 'B', 7),                           (5, 'D', 7)             ]), #scan 12
            ("R'" , [                                                                            ]),
            ("R'" , [                                                                            ]),
            ("B'" , [                                                                            ]),
                    
            ("L"  , [                                                                            ]),        
            ("F"  , [                                                                            ]),
            ("F"  , [             (2, 'U', 3),                           (5, 'L', 1)             ]), #scan 13
            ("F"  , [                                                                            ]), 
            ("F"  , [                                                                            ]), 
            ("L'" , [                                                                            ]), 
            ("L'" , [                                                                            ]), 
            ("F"  , [                                                                            ]),
            ("F"  , [             (2, 'D', 3),                           (5, 'L', 7)             ]), #scan 14
            ("F"  , [                                                                            ]),
            ("F"  , [                                                                            ]),
            ("L"  , [                                                                            ])
            ]
    
        if not os.path.exists(data_file):
            raise(ValueError("Scan data file does not exist"))
        else:
            infile = open(data_file,'rb')
            self.key_regions = pickle.load(infile)
            infile.close()        
        
        self.faces = {
            'F' : ['r' for i in range(9)],
            'R' : ['g' for i in range(9)],
            'B' : ['o' for i in range(9)],
            'L' : ['b' for i in range(9)],
            'U' : ['y' for i in range(9)],
            'D' : ['w' for i in range(9)]
            }
                
        self.camera = PiCamera()
        self.camera.resolution = (1920, 1080)
        self.camera.framerate = 15
        self.stepper_controller = StepperController()
        self.color_guesser = ColorGuesser()

    def take_snap(self, snap_no=1):
        #self.camera.start_preview()
        sleep(1)
        print("Step %d: " % snap_no)
        
        snap_loc = "temp/pi_snap_%d.jpg"%snap_no
        self.camera.capture(snap_loc)
        #camera.stop_preview()
        return snap_loc        
        
    def guess_color(self, region):
        return self.color_guesser.guess(region)
    
    def scan(self, speed = 1, interval = 1, debug = False): 
        fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
        print("Scanning started")
        
        scan_no = 1
        snap_no = 1          
       
        for ms in self.move_sequence:
            move = ms[0]
            scans = ms[1]
            print(move)
            print(scans)
            print("Scan no : %d" % scan_no)
            scan_no += 1
            
            self.stepper_controller.run(move, speed = speed)
            sleep(interval)
                  
            if len(scans) > 0:                        
                snap_loc = self.take_snap(snap_no)                
                
                snap = Image.open(snap_loc)                
                
                for sd in scans:
                    region = self.key_regions[sd[0]]
                    face   = sd[1]
                    pos    = sd[2]
                    
                    box    = snap.crop(region)
                    color  = self.guess_color(box)           
                    self.faces[face][pos] = color
                    
                    if debug:
                        draw = ImageDraw.Draw(snap)
                        draw.rectangle(region, fill=(255, 255, 255, 255))
                        draw.text((region[0], region[1]), color, fill=(255, 0, 0, 255), font = fnt)
                        del draw
                        snap.save("temp/pi_snap_marked_%d.jpg"%snap_no)
                
                snap_no+=1
                
##                cube_string = ''
##                for f in ['U', 'L', 'F', 'R', 'B', 'D']:
##                    for pos in range(9):
##                        cube_string +=  self.faces[f][pos]
##                print(cube_string)
##                sleep(10)
             
        print("Scanning ended")
        
        cube_string = ''
        for f in ['U', 'L', 'F', 'R', 'B', 'D']:
            for pos in range(9):
                cube_string +=  self.faces[f][pos]

        print(cube_string)
        
        return cube_string
