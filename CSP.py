from collections import deque

class ConstraintSatisfactionProblem:
    def __init__(self, problem, MRV, DH, LCV, infer):
        self.csp = problem
        self.possibility_dict = {}

        # heuristic selection
        self.mrv = MRV
        self.dh = DH
        self.lcv = LCV
        self.infer = infer

        # if dh turned on, but mrv is not
        if self.dh and not self.mrv:
            print("NOTE: Automatically turning on MRV to use with DH.")
            self.mrv = True

        # setting up the dictionary containing the possible domain values for each variables
        for key in problem.adjacencyList:
            self.possibility_dict[key] = list(problem.int_to_domain.keys())     # each territory starts off with all values in the domain being possibilities

        n = len(self.csp.variables)
        
        arc_q = set()
        # for each variable
        for i in self.csp.variables:
            # and for each neighbor of that variable
            for j in self.csp.adjacencyList[i]:
                # we get a pair of adjacent variables
                pair = (i, j)
                arc_q.add(pair)

        self.arc_set = arc_q
        self.test = 0
    


    # MRV
    def minimum_remaining_values(self, assignment):
        min_moves = float('inf')
        mrv = []

        for key in self.possibility_dict:
            # if this key already has an assignment
            if assignment[key] is not None:
                continue

            possible_values = self.possibility_dict[key]

            if len(possible_values) < min_moves:
                mrv = []                            # start list from scratch whenever we find a better mrv candidate
                min_moves = len(possible_values)
                mrv.append(key)
            
            # ties for degree heuristic to handle
            elif len(possible_values) == min_moves: # if this move is tied with the current mrv candidate
                mrv.append(key)                     # put them in together

        return mrv



    # degree heuristic
    def degree_heuristic(self, assignment, mrv):
        dh = 0
        max_constraints = -float('inf')

        # break ties for mrv
        for key in mrv:
            constraints = 0
            neighbors = self.csp.adjacencyList[key]

            # number of constraints = number of unassigned neighbors
            for neighbor in neighbors:
                # number of constraints = number of unassigned neighbors
                if assignment[neighbor] is None:
                    constraints += 1
            
            # if constraints set by current vertex is more than the max, update
            if constraints > max_constraints:
                max_constraints = constraints
                dh = key

        return dh



    def select_unassigned_variable(self, assignment):
        mrv = []

        # run mrv only
        if self.mrv and not self.dh:
            mrv = self.minimum_remaining_values(assignment)

        # run mrv followed by dh
        elif self.mrv and self.dh:
            dh = self.degree_heuristic(assignment, self.minimum_remaining_values(assignment))
            return dh

        # regular unassigned variable selection
        elif not self.mrv and not self.dh:
            index = 0
            for var in assignment:
                if var is None:
                    break
                index += 1
            return index

        # if dh turned off but mrv turned on then just return the first (tied) mrv
        return mrv[0]



    def least_constraining_value(self, variable):
        lcv = {}
    
        for domain in self.possibility_dict[variable]:
            # neighbors post-reduction
            neighbors = self.csp.adjacencyList[variable]

            constraints = 0
            for neighbor in neighbors:
                # if neighbor could have been assigned the domain value, then it gets constrained by the assignment
                if domain in self.possibility_dict[neighbor]:
                    # 1 more neighbor constrained by this domain choice for the variable
                    constraints += 1
            
            lcv[domain] = constraints
                
        # sort the dict by the values (number of neighbors constrained)
        sortedLCV = sorted(lcv, key=lcv.get)
        return sortedLCV



    # after making an assignment, remove the value from the posibilities of its neighbors
    # remove all but the chosen value for the variable in concern
    def reduce_possibilities(self, variable, value, assignment):
        neighbors = self.csp.adjacencyList[variable]            # neighbors of the variable we are changing
        changed = [variable]                                    # list of variables we are changing the possible domains of

        for neighbor in neighbors:
            # go through all the neighbors of the variable and remove this value from its possible values
            if assignment[neighbor] is None and value in self.possibility_dict[neighbor]:
                self.possibility_dict[neighbor].remove(value)
                changed.append(neighbor)
        
        # remove all other values from the possibility list for the current variable
        prev_possibilities = self.possibility_dict[variable]
        self.possibility_dict[variable] = [value]

        # return the list of variables whose domains have been changed
        return (changed, prev_possibilities)
        



    # undo everything done above
    def increase_possibilities(self, variable, value, assignment, changed, prev_possibilities):
        neighbors = self.csp.adjacencyList[variable]

        for neighbor in neighbors:
            # go through all the unassigned neighbors of the variable and add this value to its possible values
            if assignment[neighbor] is None and neighbor in changed:
                self.possibility_dict[neighbor].append(value)
        
        self.possibility_dict[variable] = prev_possibilities



    # order the domain values given to the backtracking algorithm
    def order_domain_values(self, variable):
        domainList = []

        # order by least constraining values first
        if self.lcv:
            domainList = self.least_constraining_value(variable)      

        # regular order 
        else:
            domainList = list(self.csp.int_to_domain.keys())

        return domainList



    # check if all assignments have been made
    def assignment_is_complete(self, assignment):
        for val in assignment:      
            if val is None:
                return False
        return True



    def backtracking_search(self):
        init_assingment = [None for i in range(len(self.csp.int_to_variable))]
        return self.backtrack(init_assingment, self.csp)

    

    def backtrack(self, assignment, csp):
        csp.visited += 1
        
        if self.assignment_is_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        domains = self.order_domain_values(variable)

        for value in domains:
            if csp.is_consistent(variable, value, assignment):                                            # check if value works with variable in current assignment
                assignment[variable] = value
                (changed, prev_possibilities) = self.reduce_possibilities(variable, value, assignment)    # update possibility dict used by heuristics

                # if inference turned on
                if self.infer:
                    # make an inference
                    removedDict = self.arc_consistency_3()
                    # check if inference is valid
                    valid = self.check_inference()

                    # if inference is successful
                    if valid:
                        # add valid inferences to assignment
                        prev_possibilities = self.add_inference_to_assignment(assignment)

                        # check if we get result from inference
                        result = self.backtrack(assignment, csp)
                        if result is not False:
                            return result

                        # if results in failure, remove inferences from assignment
                        for var in prev_possibilities:
                            assignment[var] = prev_possibilities[var]
                    
                    # add values back to domain
                    for var in removedDict:
                        for val in removedDict[var]:
                            self.possibility_dict[var].append(val)
                            
                # if inference is not turned on
                else:
                    result = self.backtrack(assignment, csp)
                    if result is not False:
                        return result                

                self.increase_possibilities(variable, value, assignment, changed, prev_possibilities)     # undo the changes made to the possibility dict by the failed assignment
                assignment[variable] = None                                                               # undo the failed assignment
                
        # return failure
        return False

    def add_inference_to_assignment(self, assignment):
        prev_poss = {}

        for variable in self.possibility_dict:
            domains = self.possibility_dict[variable]
            
            # if we narrowed it down to only one possible value for a variable
            # add inference to assignment
            if len(domains) == 1 and assignment[variable] is None:
                prev_poss[variable] = assignment[variable]
                assignment[variable] = domains[0]

        return prev_poss

                

    def check_inference(self):
        for variable in self.possibility_dict:
            # the possible domains of each variable
            domains = self.possibility_dict[variable]

            # if there are no possible domain values for a variable
            # inference has failed
            if len(domains) < 1:
                return False
        
        return True


    # set of arcs, so you don't add the arc more than once
    def arc_consistency_3(self):
        # initialized to all arcs
        queue = deque()
        removedDict = {}

        for pair in self.arc_set:
            queue.append(pair)

        while queue:
            pair = queue.popleft()
            x_i = pair[0]
            x_j = pair[1] 

            # if pair is inconsistent and inconsistent domain values were removed
            removed = self.remove_inconsistent_variables(x_i, x_j, removedDict)

            # if some domain was removed from x_i
            if removed:
                # add the neighbors of x_i to the queue again
                for x_k in self.csp.adjacencyList[x_i]:
                    pair = (x_k, x_i)
                    queue.append(pair)
        
        return removedDict


    def remove_inconsistent_variables(self, x_i, x_j, removedDict):
        removed = False
        for x in self.possibility_dict[x_i]:

            # if x_j is a neighbor of x_i and the current domain value of x is the only possible domain of x_j
            if x_j in self.csp.adjacencyList[x_i] and self.possibility_dict[x_j] == [x]:
            
                # remove x from domain of x_i
                self.possibility_dict[x_i].remove(x)
                removed = True

                if x_i not in removedDict:
                    removedDict[x_i] = []
                if x_i in removedDict:
                    removedDict[x_i].append(x)        

        return removed    

    