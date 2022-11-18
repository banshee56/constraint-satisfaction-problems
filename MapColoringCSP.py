from CSP import ConstraintSatisfactionProblem


class MapColoringCSP:
    def __init__(self, filename):
        (adjacencyList, domainList) = self.get_params(filename)

        self.domain = domainList

        variables = []              # variables in int form
        int_to_variable = {}       # int to variables map 
        territory_to_int = {}       # variables to int map
        i = 0
        for variable in adjacencyList:
            variables.append(i)
            int_to_variable[i] = variable
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
        self.int_to_variable = int_to_variable        # map from ints to original variables
        self.int_to_domain = colorDict                  # map from ints to original color values
        self.visited = 0                                # number of nodes visited

    
    # reads from a file containing the information
    def get_params(self, filename):
        file = open(filename, 'r')
        domain_list = file.readline().strip().split(',')

        adjacency_list = {} # dictionary
        for line in file:
            states = line.strip().split(',')
            curr = states[0]
            neighbors = set()
            for neighbor in states[1:]:
                neighbors.add(neighbor)

            if len(neighbors) > 0:
                adjacency_list[curr] = neighbors
            else:
                adjacency_list[curr] = []

        file.close()

        return (adjacency_list, domain_list)

    def solve_csp(self, MRV=False, DH=False, LCV=False, infer=False):
        csp = ConstraintSatisfactionProblem(self, MRV, DH, LCV, infer)

        # int csp solution
        solution = csp.backtracking_search()

        if not solution:
            print('No solution found after visiting '+str(self.visited)+' nodes.')
            return False

        # map from int back to variables
        readable = {}
        for variable in range(len(solution)):
            value = solution[variable]
            readable[self.int_to_variable[variable]] = self.int_to_domain[value]

        # return solution
        print('Found solutions after visiting '+str(self.visited)+' nodes.')
        return readable

    def is_consistent(self, variable, value, assignment):
        neighbors = self.adjacencyList[variable]
        
        for neighbor in neighbors:
            if value == assignment[neighbor]:
                return False

        return True

    def pair_consistent(self, var1, var2, val1, val2):
        # if variables are not neighbors
        if var1 not in self.adjacencyList[var2]:
            # then they don't constrain each other
            return True

        # if they are neighbors and their domain values are the same
        if val1 == val2:
            # then they are inconsistent
            return False
        
        return True
