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

    def solve_csp(self, MRV=False, DH=False, LCV=False):
        csp = ConstraintSatisfactionProblem(self, MRV, DH, LCV)

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

    def is_consistent(self, variable, value, assignment):
        neighbors = self.adjacencyList[self.int_to_territory[variable]]
        
        for neighbor in neighbors:
            neighbor_int = self.territory_to_int[neighbor]

            if value == assignment[neighbor_int]:
                return False

        return True