from CSP import ConstraintSatisfactionProblem


class MapColoringCSP:
    def __init__(self, adjacencyList, domainList):
        self.adjacencyList = adjacencyList


        variables = []
        for key in adjacencyList:
            variables.append(key)

        self.variables =  variables
        self.domain = domainList

        territoryDict1 = {}
        territoryDict2 = {}
        index = 0
        for variable in variables:
            territoryDict1[index] = variable
            territoryDict2[variable] = index
            index += 1

        self.int_to_territory = territoryDict1
        self.territory_to_int = territoryDict2

        colorDict = {}
        index = 0
        for color in domainList:
            colorDict[index] = color
            index += 1

        self.int_to_domain = colorDict
        self.visited = 0

    def solve_csp(self):
        csp = ConstraintSatisfactionProblem(self)

        # int csp solution
        solution = csp.backtracking_search()

        if not solution:
            print('No solution found after visiting '+str(self.visited)+' nodes.')
            return False

        # map from int back to variables
        # TO DO
        readable = {}
        for variable in range(len(solution)):
            value = solution[variable]
            readable[self.int_to_territory[variable]] = self.int_to_domain[value]

        # return solution
        print('Found solutions after visiting '+str(self.visited)+' nodes.')
        return readable

    def order_domain_values(self, variable, assignment):
        domain = []
        
        for num in self.int_to_domain:
            domain.append(num)

        return domain

    def is_consistent(self, variable, value, assignment):
        neighbors = self.adjacencyList[self.int_to_territory[variable]]
        
        for neighbor in neighbors:
            neighbor_int = self.territory_to_int[neighbor]

            if len(assignment) > neighbor_int and value == assignment[neighbor_int]:
                return False

        return True

    # def is_consistent(self, variable, value, assignment):
        # WA
        if variable == 0:
            # NT and SA
            if len(assignment) > 1 and value == assignment[1]:
                return False
            if len(assignment) > 2 and value == assignment[2]:
                return False
            
        # NT 
        if variable == 1:
            # WA, SA, Q
            if len(assignment) > 0 and value == assignment[0]:
                return False
            if len(assignment) > 2 and value == assignment[2]:
                return False
            if len(assignment) > 3 and value == assignment[3]:
                return False

        # SA
        if variable == 2:
            # WA, NT, Q
            if len(assignment) > 0 and value == assignment[0]:
                return False
            if len(assignment) > 1 and value == assignment[1]:
                return False
            if len(assignment) > 3 and value == assignment[3]:
                return False

        # Q
        if variable == 3:
            # NT, SA, NSW
            if len(assignment) > 1 and value == assignment[1]:
                return False
            if len(assignment) > 2 and value == assignment[2]:
                return False
            if len(assignment) > 4 and value == assignment[4]:
                return False

        # NSW
        if variable == 4:
            # SA, Q, V
            if len(assignment) > 2 and value == assignment[2]:
                return False
            if len(assignment) > 3 and value == assignment[3]:
                return False
            if len(assignment) > 5 and value == assignment[5]:
                return False

        # V
        if variable == 5:
            # SA, NSW
            if len(assignment) > 2 and value == assignment[2]:
                return False
            if len(assignment) > 4 and value == assignment[4]:
                return False
    
        # # T
        # if variable == 6:
        #     # nothing

        return True