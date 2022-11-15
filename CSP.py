from queue import Queue

class ConstraintSatisfactionProblem:
    def __init__(self, problem, MRV, DH, LCV):
        self.csp = problem
        self.possibility_dict = {}

        # heuristic selection
        self.mrv = MRV
        self.dh = DH
        self.lcv = LCV

        # if dh turned on, but mrv is not
        if self.dh and not self.mrv:
            print("NOTE: Automatically turning on MRV to use with DH.")
            self.mrv = True

        # setting up the dictionary containing the possible domain values for each variables
        for key in problem.adjacencyList:
            self.possibility_dict[key] = list(problem.int_to_domain.keys())     # each territory starts off with all values in the domain being possibilities

        n = len(self.csp.variables)
        
        # arc_q = Queue(maxsize=n**2)
        # for i in self.csp.variables

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

    

    def least_constraining_value(self, variable, assignment):
        lcv = {}
    
        for domain in self.possibility_dict[variable]:
            changed = self.reduce_possibilities(variable, domain, assignment)

            # neighbors post-reduction
            neighbors = self.csp.adjacencyList[variable]
            sum = 0
            for neighbor in neighbors:
                # when assigning variable to the current domain, we can get a sum of the possible values available for its neighbors
                sum += len(self.possibility_dict[neighbor])
            
            lcv[domain] = sum
            self.increase_possibilities(variable, domain, assignment, changed)
                
        # sort the dict by the values (sums) and then add the keys (domains) to the domain list
        sortedLCV = sorted(lcv, key=lcv.get, reverse=True)
        return sortedLCV



    # after making an assignment, remove the value from the posibilities of its neighbors
    # remove all but the chosen value for the variable in concern
    def reduce_possibilities(self, variable, value, assignment):
        neighbors = self.csp.adjacencyList[variable]
        # list of vertices we changed the domains of
        changed = []

        for neighbor in neighbors:
            # go through all the neighbors of the variable and remove this value from its possible values
            if assignment[neighbor] is None and value in self.possibility_dict[neighbor]:
                self.possibility_dict[neighbor].remove(value)
                changed.append(neighbor)

        return changed
        
        # we would remove all other values from the possibility list for the current variable
        # but mrv does not even consider the possibilities of variables that are already assigned
        # so no need to change the possibilities here, it would just add extra work having to add them back later in increase_possibilities



    # undo everything done above
    def increase_possibilities(self, variable, value, assignment, changed):
        neighbors = self.csp.adjacencyList[variable]

        for neighbor in neighbors:
            # go through all the unassigned neighbors of the variable and add this value to its possible values
            if assignment[neighbor] is None and neighbor in changed:
                self.possibility_dict[neighbor].append(value)



    # maybe use LCV here
    def order_domain_values(self, variable, assignment):
        domainList = []

        if self.lcv:
            domainList = self.least_constraining_value(variable, assignment)       
        else:
            # for num in self.csp.int_to_domain:
            domainList = list(self.csp.int_to_domain.keys())

        return domainList



    def assignment_is_complete(self, assignment):
        for val in assignment:
            if val is None:
                return False
        return True



    def backtracking_search(self):
        init_assingment = [None for i in range(len(self.csp.int_to_territory))]
        return self.recursive_backtracking(init_assingment, self.csp)

    

    def recursive_backtracking(self, assignment, csp):
        csp.visited += 1
        if self.assignment_is_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        domains = self.order_domain_values(variable, assignment)
        for value in domains:
            # check if value works with variable in current assignment
            if csp.is_consistent(variable, value, assignment):
                # variable is index
                assignment[variable] = value

                # update possibility dict used by heuristics
                changed = self.reduce_possibilities(variable, value, assignment)
                result = self.recursive_backtracking(assignment, csp)

                if result is not False:
                    return result
                
                self.increase_possibilities(variable, value, assignment, changed)
                assignment[variable] = None
                
        # return failure
        return False



    # set of arcs, so you don't add the arc more than once
    # def arc_consistency_3():
    #     arc_q = Queue()
    


