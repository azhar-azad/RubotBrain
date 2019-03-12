from rubik_solver.RubiksSolver import RubiksSolver   
   
cubestring = "worryrbyybyrwgrrygwbrbrgogwbwgybbogbwgooobyoyyrgowwgwo"
rubiks_solver = RubiksSolver()
solution = rubiks_solver.solve(cubestring, 'Kociemba')
print(solution)
