from MapColoringCSP import MapColoringCSP
from time import time


# edit switches here
filename = 'us_states.txt'          # input file, see README.md for formatting information
compareHeuristics = True            # set to True to run tests with heuristics enabled
inference = True                    # set to True to run tests with arc consistency





# running test without heuristics
if not compareHeuristics:
    # solve the problem normally, with no heuristics
    mapColoringProblem = MapColoringCSP(filename)
    before = time()

    # parameters: MRV (true or false), DH (true or false), LCV (true or false), infer (true or false)
    solution = mapColoringProblem.solve_csp(infer=inference)
    after = time()

    if solution:
        print(solution)
        print("It took "+str(after-before)+" seconds to solve.")

# running tests with heurisitcs
else:
    if inference:
        print("For the following heuristics, inference is enabled")
    else:
        print("For the following heuristics, inference is disabled")
    
    before = time() # to calculate time taken for all tests

    # with only mrv heuristic
    print()
    print("Running with only MRV")
    mapColoringProblem = MapColoringCSP(filename)
    only_mrv = mapColoringProblem.solve_csp(MRV=True, infer=inference)
    print("Only MRV: "+str(only_mrv))

    # with both mrv and dh
    print()
    print("Running with both MRV and DH")
    mapColoringProblem = MapColoringCSP(filename)
    mrv_dh = mapColoringProblem.solve_csp(MRV=True, DH=True, infer=inference)

    mapColoringProblem = MapColoringCSP(filename)
    print("Running with only DH")
    # only turning on dh will automatically turn on the switch for mrv
    only_dh = mapColoringProblem.solve_csp(DH=True, infer=inference)
    print("MRV and DH: "+str(mrv_dh))

    # with both mrv and lcv
    print()
    print("Running with MRV and LCV")
    mapColoringProblem = MapColoringCSP(filename)
    mrv_lcv = mapColoringProblem.solve_csp(MRV=True, LCV=True, infer=inference)
    print("MRV and LCV: "+str(mrv_lcv))

    # with only lcv
    print()
    print("Running with only LCV")
    mapColoringProblem = MapColoringCSP(filename)
    only_lcv = mapColoringProblem.solve_csp(LCV=True, infer=inference)
    print("Only LCV: "+str(only_lcv))

    after = time()

    # comparing results from turning on both MRV and DH and from turning on just DH 
    # should give same result for reason in comment in Line 47
    print()
    print("Comparing results...")
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

    print()
    print("The above tests took "+ str(after-before) + " seconds.")


    

    
   

