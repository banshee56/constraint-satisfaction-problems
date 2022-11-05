class ConstraintSatisfactionProblem:
    def __init__(self, problem):
        self.csp = problem
        self.possibility_dict = {}

        for key in problem.int_to_territory:
            self.possibility_dict[key] = list(problem.int_to_domain.keys())
    
    # MRV and degree heuristics
    def select_unassigned_variable(self, assignment):
        mrv = []
        if self.csp.mrv:
            min_moves = float('inf')

            for key in self.possibility_dict:
                # if this key already has an assignment
                if assignment[key] is not None:
                    continue

                possible_values = self.possibility_dict[key]

                if len(possible_values) < min_moves:
                    mrv = []
                    min_moves = len(possible_values)
                    mrv.append(key)
                
                # ties for degree heuristic to handle
                elif len(possible_values) == min_moves:
                    mrv.append(key)

            # if not paired with degree heuristic, just send one of the tied variables as answer
            if not self.csp.dh:
                return mrv[0]

        if self.csp.dh:
            dh = 0
            max_constraints = -float('inf')

            # break ties
            if self.csp.mrv:
                neighbors = []
                for key in mrv:
                    constraints = 0
                    neighbors = self.csp.adjacencyList[self.csp.int_to_territory[key]]
                
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
                    
                    if constraints > max_constraints:
                        max_constraints = constraints
                        dh = key

            # print(self.csp.int_to_territory[dh])
            return dh

        # regular unassigned variable selection
        else:
            index = 0
            for var in assignment:
                if var is None:
                    break
                index += 1
            return index

        # return len(assignment)

    # LCV
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
                possible_values = self.possibility_dict[variable]
                if value in possible_values:
                    possible_values.remove(value)

                result = self.recursive_backtracking(assignment, csp)

                if result is not False:
                    return result
                
                # assignment.pop()
                assignment[variable] = None
                possible_values.append(value)

        # return failure
        return False