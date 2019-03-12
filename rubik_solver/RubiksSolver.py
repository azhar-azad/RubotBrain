from __future__ import print_function
import argparse
import time
from past.builtins import basestring

try:
    from .Solver import Solver
except (SystemError, ImportError):
    from Solver import Solver
    
try:
    from .Solver import Beginner
except (SystemError, ImportError):
    from Solver import Beginner
    
try:
    from .Solver import CFOP
except (SystemError, ImportError):
    from Solver import CFOP
    
try:    
    from .Solver import Kociemba
except (SystemError, ImportError):
    from Solver import Kociemba

try:
    from .NaiveCube import NaiveCube
except (SystemError, ImportError):
    from NaiveCube import NaiveCube
    
try:
    from .Cubie import Cube
except (SystemError, ImportError):
    from Cubie import Cube

try:
    from .Printer import TtyPrinter
except (SystemError, ImportError):
    from Printer import TtyPrinter

class RubiksSolver(object):

    METHODS = {
        'Beginner': Beginner.BeginnerSolver,
        'CFOP': CFOP.CFOPSolver,
        'Kociemba': Kociemba.KociembaSolver
    }
    
    def is_valid_cube(self, cube):
        '''Checks if cube is one of str, NaiveCube or Cubie.Cube and returns
        an instance of Cubie.Cube'''
        is_valid = True

        if isinstance(cube, basestring):
            c = NaiveCube()
            c.set_cube(cube)
            cube = c

        if isinstance(cube, NaiveCube):
            c = Cube()
            c.from_naive_cube(cube)
            cube = c

        if not isinstance(cube, Cube):
            is_valid = False

        return is_valid

    def check_valid_cube(self, cube):
        '''Checks if cube is one of str, NaiveCube or Cubie.Cube and returns
        an instance of Cubie.Cube'''

        if isinstance(cube, basestring):
            c = NaiveCube()
            c.set_cube(cube)
            cube = c

        if isinstance(cube, NaiveCube):
            c = Cube()
            c.from_naive_cube(cube)
            cube = c

        if not isinstance(cube, Cube):
            raise ValueError('Cube is not one of (str, NaiveCube or Cubie.Cube)')

        return cube

    def solve(self, cube, method = Beginner.BeginnerSolver, *args, **kwargs):
        
        print(method)
        if isinstance(method, basestring):
            if not method in RubiksSolver.METHODS:
                raise ValueError('Invalid method name, must be one of (%s)' % ', '.join(RubiksSolver.METHODS.keys()))
            
            method = RubiksSolver.METHODS[method]

        if not issubclass(method, Solver):
            raise ValueError('Method %s is not a valid Solver subclass' %
                method.__class__.__name__
            )

        cube = self.check_valid_cube(cube)

        solver = method(cube)

        return solver.solution(*args, **kwargs)

    def print_cube(self, cube, color = True):
        cube = self.check_valid_cube(cube)
        printer = TtyPrinter(cube, color)
        printer.pprint()



