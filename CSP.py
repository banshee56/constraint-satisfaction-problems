class ConstraintSatisfactionProblem:
    def __init__(self, problem, MRV, DH, LCV):
        self.csp = problem
        self.possibility_dict = {}

        # heuristic selection
        self.mrv = MRV
        self.dh = DH
        self.lcv = LCV

        for key in problem.int_to_territory:
            # each territory starts off with all values in the domain being possibilities
            self.possibility_dict[key] = list(problem.int_to_domain.keys())
    
    # MRV
    def minimum_remaining_values(self, assignment):
        min_moves = float('inf')

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

        # # if not paired with degree heuristic, just send one of the tied variables as answer
        # if not self.dh:
        return mrv

    # degree heuristic
    def degree_heuristic(self, assignment, mrv):
        dh = 0
        max_constraints = -float('inf')

        # break ties if more than one mrv
        if len(mrv) > 1:
            neighbors = []
            for key in mrv:
                constraints = 0
                neighbors = self.csp.adjacencyList[self.csp.int_to_territory[key]]

                # number of constraints = number of unassigned neighbors
                for n in neighbors:
                    neighbor = self.csp.territory_to_int[n]
                    if assignment[neighbor] is None:
                        constraints += 1
                
                if constraints > max_constraints:
                    max_constraints = constraints
                    dh = key

        # run dh on all vertices
        else:
            for key in self.possibility_dict:
                if assignment[key] is not None:
                    continue
                constraints = 0

                neighbors = self.csp.adjacencyList[self.csp.int_to_territory[key]]
                for n in neighbors:
                    neighbor = self.csp.territory_to_int[n]
                    if assignment[neighbor] is None:
                        constraints += 1
                    print("key "+str(neighbor)+" has constraints: "+str(constraints))
                
                if constraints > max_constraints:
                    max_constraints = constraints
                    dh = key

        # print(self.csp.int_to_territory[dh])
        print("dh returning: "+str(dh))
        return dh

    def select_unassigned_variable(self, assignment):
        mrv = []
        if self.mrv:
            mrv = self.minimum_remaining_values(assignment)

        if self.dh:
            print(mrv)
            dh = self.degree_heuristic(assignment, mrv)
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

    # maybe use LCV here
    def order_domain_values(self, variable, assignment):
        domain = []
        
        for num in self.csp.int_to_domain:
            domain.append(num)

        return domain

    def assignment_is_complete(self, assignment, csp):
        for val in assignment:
            if val is None:
                return False
        return True
        # return len(assignment) == len(csp.int_to_territory)

    def backtracking_search(self):
        init_assingment = [None for i in range(len(self.csp.int_to_territory))]
        return self.recursive_backtracking(init_assingment, self.csp)
    
    def recursive_backtracking(self, assignment, csp):
        csp.visited += 1
        if self.assignment_is_complete(assignment, csp):
            return assignment

        variable = self.select_unassigned_variable(assignment)

        domains = self.order_domain_values(variable, assignment)
        for value in domains:
            # check if value works with variable in current assignment
            if csp.is_consistent(variable, value, assignment):
                # variable is index
                # assignment.append(value)
                assignment[variable] = value
                # possibility dict used by heuristics
                self.reduce_possibilities(variable, value, assignment)

                result = self.recursive_backtracking(assignment, csp)

                if result is not False:
                    return result
                
                self.increase_possibilities(variable, value, assignment)
                # assignment.pop()
                assignment[variable] = None
                

        # return failure
        return False
    
    # after making an assignment, remove the value from the posibilities of its neighbors
    # remove all but the chosen value for the variable in concern
    
    def reduce_possibilities(self, variable, value, assignment):
        adjList = self.csp.adjacencyList

        neighbors = adjList[self.csp.int_to_territory[variable]]
        for n in neighbors:
            neighbor = self.csp.territory_to_int[n]

            # go through all the neighbors of the variable and remove this value from its possible values
            if assignment[neighbor] is None and value in self.possibility_dict[neighbor]:
                self.possibility_dict[neighbor].remove(value)
        
        # we would remove all other values from the possibility list
        # but mrv does not even consider the possibilities of variables that are already assigned
        # so no need to change the possibilities here, it would just add extra work having to add them back later in increase_possibilities

    # undo everything done above
    def increase_possibilities(self, variable, value, assignment):
        adjList = self.csp.adjacencyList

        neighbors = adjList[self.csp.int_to_territory[variable]]
        for n in neighbors:
            neighbor = self.csp.territory_to_int[n]

            # go through all the neighbors of the variable and add this value to its possible values
            if assignment[neighbor] is None and value in self.possibility_dict[neighbor]:
                self.possibility_dict[neighbor].append(value)

# set of arcs, so you don't add the arc more than once