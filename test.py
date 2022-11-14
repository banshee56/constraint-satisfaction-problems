from MapColoringCSP import MapColoringCSP
from time import time

# reads from a file containing the information
def get_params(file):
    domain_list = file.readline().strip().split(',')

    adjacency_list = {} # dictionary
    for line in file:
        states = line.strip().split(',')
        curr = states[0]
        neighbors = set()
        for neighbor in states[1:]:
            neighbors.add(neighbor)

        if len(neighbors) > 0:
            adjacency_list[curr] = neighbors
        else:
            adjacency_list[curr] = []

    return (adjacency_list, domain_list)

# edit filename for input
file = open('us_states.txt', 'r')
(adjacency_list, domain_list) = get_params(file)

compareHeuristics = True

if not compareHeuristics:
    mapColoringProblem = MapColoringCSP(adjacency_list, domain_list)
    before = time()
    # parameters: MRV (true or false), DH (true or false), LCV (true or false)
    solution = mapColoringProblem.solve_csp(MRV=True, LCV=True)
    after = time()

    if solution:
        print(solution)
        print("It took "+str(after-before)+" seconds to solve.")
        
else:
    mapColoringProblem = MapColoringCSP(adjacency_list, domain_list)
    # with only mrv heuristic
    print("Running with only MRV")
    only_mrv = mapColoringProblem.solve_csp(MRV=True)

    print()
    mapColoringProblem = MapColoringCSP(adjacency_list, domain_list)
    print("Running with both MRV and DH")
    # with both mrv and dh
    mrv_dh = mapColoringProblem.solve_csp(MRV=True, DH=True)

    mapColoringProblem = MapColoringCSP(adjacency_list, domain_list)
    print("Running with only DH")
    # only turning on dh will automatically turn on the switch for mrv
    only_dh = mapColoringProblem.solve_csp(DH=True)

    mapColoringProblem = MapColoringCSP(adjacency_list, domain_list)
    print("Running with MRV and LCV")
    # only turning on dh will automatically turn on the switch for mrv
    mrv_lcv = mapColoringProblem.solve_csp(MRV=True, LCV=True)

    # comparing results from turning on both MRV and DH and from turning on just DH 
    # should give same result for reason in comment in Line 47
    print()
    print("Comparing results")
    if mrv_dh != only_dh:
        print("Error: these should return the same results.")
    else:
        print("Turning on DH gives same result as turning on both MRV and DH. This was intended.")

    # chekcing if turning on DH made a difference
    if only_mrv != mrv_dh:
        print("Result with only MRV differs from result with both MRV and DH.")
    else:
        print("Turning on DH did not change the result from only working with MRV.")

    # checking if doing LCV on top of MRV changes the result of only MRV
    if only_mrv != mrv_lcv:
        print("Result with only MRV differs from result with both MRV and LCV.")
    else:
        print("Result with only MRV same as result with both MRV and LCV.")


    

    
   

