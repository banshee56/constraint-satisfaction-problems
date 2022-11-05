class ConstraintSatisfactionProblem:
    def __init__(self, problem):
        self.csp = problem
        self.constraint_dict = {}

        for key in problem.int_to_territory:
            self.constraint_dict[key] = list(problem.int_to_domain.keys())
    
    # MRV and degree heuristics
    def select_unassigned_variable(self, assignment):
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

                result = self.recursive_backtracking(assignment, csp)

                if result is not False:
                    return result
                
                # assignment.pop()
                assignment[variable] = None

        # return failure
        return False