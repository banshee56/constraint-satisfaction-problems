from CSP import ConstraintSatisfactionProblem


class MapColoringCSP:
    def __init__(self, adjacencyList, domainList):
        self.adjacencyList = adjacencyList

        # self.variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
        # self.domain = ['r', 'g', 'b']
        variables = []

        for key in adjacencyList:
            variables.append(key)

        self.variables =  variables
        self.domain = domainList

        # self.int_to_territory = {0: 'WA', 1:'NT', 2:'SA', 3:'Q', 4:'NSW', 5:'V', 6:'T'}
        # self.int_to_domain = {0: 'r', 1:'g', 2:'b'}
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

        state = [None for i in range(len(self.variables))] 
        # for i in range(len(self.variables)):
        #     state.append(None)
        
        self.state = state

    def solve_csp(self):
        csp = ConstraintSatisfactionProblem(self)

        # int csp solution
        solution = csp.backtracking_search()

        if not solution:
            return False

        # map from int back to variables
        # TO DO
        readable = {}
        for variable in range(len(solution)):
            value = solution[variable]
            readable[self.int_to_territory[variable]] = self.int_to_domain[value]

        # return solution
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