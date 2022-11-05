class ConstraintSatisfactionProblem:
    def __init__(self, problem):
        self.csp = problem
    
    def select_unassigned_variable(self, assignment):
        return len(assignment)

    def assignment_is_complete(self, assignment, csp):
        return len(assignment) == len(csp.int_to_territory)

    def backtracking_search(self):
        # init_assingment = [None for i in range(len(self.csp.int_to_territory))]
        return self.recursive_backtracking([], self.csp)
    
    def recursive_backtracking(self, assignment, csp):
        csp.visited += 1
        if self.assignment_is_complete(assignment, csp):
            return assignment

        variable = self.select_unassigned_variable(assignment)

        domains = csp.order_domain_values(variable, assignment)
        for value in domains:
            # check if value works with variable in current assignment
            if csp.is_consistent(variable, value, assignment):
                # variable is index
                assignment.append(value)
                # assignment[variable] = value

                result = self.recursive_backtracking(assignment, csp)

                if result is not False:
                    return result
                
                assignment.pop()
                # assignment[variable] = None

        # return failure
        return False