from CSP import ConstraintSatisfactionProblem


class MapColoringCSP:
    def __init__(self, adjacencyList, domainList):
        self.ogAdjList = adjacencyList
        self.domain = domainList

        variables = []              # variables in int form
        int_to_territory = {}       # int to variables map 
        territory_to_int = {}       # variables to int map
        i = 0
        for variable in adjacencyList:
            variables.append(i)
            int_to_territory[i] = variable
            territory_to_int[variable] = i
            i += 1
        
        # a dictionary from color int to the color domain
        colorDict = {}
        i = 0
        for color in domainList:
            colorDict[i] = color
            i += 1

        # creating an adjacency list with int counterparts instead of the original variables and domains
        adjList = {}
        for var in adjacencyList:
            neighbors = adjacencyList[var]
            adjList[territory_to_int[var]] = []

            for neighbor in neighbors:
                adjList[territory_to_int[var]].append(territory_to_int[neighbor])

        self.adjacencyList = adjList                    # adj list with ints
        self.variables =  variables                     # variables list in ints
        self.int_to_territory = int_to_territory        # map from ints to original variables
        self.int_to_domain = colorDict                  # map from ints to original color values
        self.visited = 0                                # number of nodes visited

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
        neighbors = self.adjacencyList[variable]
        
        for neighbor in neighbors:
            if value == assignment[neighbor]:
                return False

        return True