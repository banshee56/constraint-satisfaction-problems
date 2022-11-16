from collections import deque

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

    

    def least_constraining_value(self, variable, assignment):
        lcv = {}
    
        for domain in self.possibility_dict[variable]:
            (changed, prev_possibilities)  = self.reduce_possibilities(variable, domain, assignment)

            # neighbors post-reduction
            neighbors = self.csp.adjacencyList[variable]
            sum = 0
            for neighbor in neighbors:
                # when assigning variable to the current domain, we can get a sum of the possible values available for its neighbors
                sum += len(self.possibility_dict[neighbor])
            
            lcv[domain] = sum
            self.increase_possibilities(variable, domain, assignment, changed, prev_possibilities)
                
        # sort the dict by the values (sums) and then add the keys (domains) to the domain list
        sortedLCV = sorted(lcv, key=lcv.get, reverse=True)
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
    def order_domain_values(self, variable, assignment):
        domainList = []

        # order by least constraining values first
        if self.lcv:
            domainList = self.least_constraining_value(variable, assignment)      

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
        init_assingment = [None for i in range(len(self.csp.int_to_territory))]
        return self.backtrack(init_assingment, self.csp)

    

    def backtrack(self, assignment, csp):
        csp.visited += 1
        if self.assignment_is_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        domains = self.order_domain_values(variable, assignment)

        for value in domains:
            if csp.is_consistent(variable, value, assignment):                                            # check if value works with variable in current assignment
                assignment[variable] = value
                (changed, prev_possibilities) = self.reduce_possibilities(variable, value, assignment)    # update possibility dict used by heuristics

                result = self.backtrack(assignment, csp)
                if result is not False:
                    return result
                
                self.increase_possibilities(variable, value, assignment, changed, prev_possibilities)     # undo the changes made to the possibility dict by the failed assignment
                assignment[variable] = None                                                               # undo the failed assignment
                
        # return failure
        return False



    # set of arcs, so you don't add the arc more than once
    def arc_consistency_3(self):
        # initialized to all arcs
        queue = deque()
        for pair in self.arc_set:
            queue.append(pair)

        while queue:
            pair = queue.popleft()
            x_i = pair[0]
            x_j = pair[1] 

            # if pair is inconsistent and inconsistent domain values were removed
            if self.remove_inconsistent_variables(x_i, x_j):
                # add the neighbors of x_i to the queue again
                for x_k in self.csp.adjacencyList[x_i]:
                    pair = (x_k, x_i)
                    queue.append(pair)



    def remove_inconsistent_variables(self, x_i, x_j):
        removed =  False

        for x in self.possibility_dict[x_i]:
            consistent = False
            for y in self.possibility_dict[x_j]:
                # if even one x, y pair is consistent
                if self.csp.pair_consistent(x_i, x_j, x, y):
                    consistent = True
            
            # if no y in domain x_j allows (x, y) to satisfy the constraint
            if not consistent:
                # remove x from domain x_i
                self.possibility_dict[x_i].remove(x)
                removed = True
        
        return removed
