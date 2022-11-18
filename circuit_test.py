from CircuitBoardCSP import CircuitBoardCSP
from time import time

# basic problem
filename = 'circuit.txt'

# solve the problem normally
circuitProblem = CircuitBoardCSP(filename)
before = time()
# optional parameters: MRV (true or false), DH (true or false), LCV (true or false), infer (true or false)
circuitProblem.solve_csp()
after = time()

print("It took "+str(after-before)+" seconds to solve circuit in "+filename)
print()



# a harder problem, requires rearranging
filename = 'circuit2.txt'

# solve the problem normally
mapColoringProblem = CircuitBoardCSP(filename)
before = time()
# optional parameters: MRV (true or false), DH (true or false), LCV (true or false), infer (true or false)
mapColoringProblem.solve_csp()
after = time()

print("It took "+str(after-before)+" seconds to solve circuit in "+filename)
