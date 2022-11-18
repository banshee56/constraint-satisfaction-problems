from CSP import ConstraintSatisfactionProblem
from Component import Component

class CircuitBoardCSP:
    def __init__(self, filename):
        (ogAdjList, domainList, components, board) = self.get_params(filename)

        # mapping int to components
        int_to_component = {}       # int to variables map 
        component_to_int = {}       # variables to int map
        variables = []
        i = 0
        for variable in ogAdjList:
            variables.append(i)
            int_to_component[i] = variable
            component_to_int[variable] = i
            i += 1
        
        # a dictionary from color int to the color domain
        int_to_location = {}
        location_to_int = {}
        i = 0
        for location in domainList:
            int_to_location[i] = location
            location_to_int[location] = i
            i += 1

        # creating an adjacency list with int counterparts instead of the original variables and domains
        adjList = {}
        for var in ogAdjList:
            neighbors = ogAdjList[var]
            adjList[component_to_int[var]] = []

            for neighbor in neighbors:
                adjList[component_to_int[var]].append(component_to_int[neighbor])
        
        self.int_to_variable = int_to_component           # map from ints to original variables
        self.int_to_domain = int_to_location              # map from ints to original color values
        self.adjacencyList = adjList                      # adj list with ints
        self.variables =  variables                       # variables list in ints
        self.components = components                      # dict mapping chars to their components
        self.board = board                                # circuit board as a Component() object
        self.visited = 0                                  # number of nodes visited
    
    # reads from an input file containing the problem information
    def get_params(self, filename):
        file = open(filename, 'r')

        # dimensions of the circuit board
        dim = file.readline().strip().split('x')
        length = int(dim[0])-1
        height = int(dim[1])-1

        # the circuit board
        board = Component('.', length, height)

        domain_list = []
        # adding all the possible locations on the grid to the domain list
        for l in range(length+1):
            for w in range(height+1):
                domain_list.append((l, w))

        components = {}
        variables = []
        adjacency_list = {}     # dictionary
        prev_char = '.'         # last char we saw in the file, init to '.'
        
        for line in file:
            line = list(line.strip())
            char = line[0]

            # new character found
            if char != prev_char:
                # create a component for the character
                length = len(line)
                height = 1
                # Component object has the associated char and the length and height of the component
                comp = Component(char, length, height)

                # add component to components dict
                components[char] = comp

                # add character of the component to list of variables to represent component
                variables.append(char)
                prev_char = char        # remember that this char was the last char we saw
            
            # if we saw this character before
            else:
                # if we found a '.', quit because this is invalid
                if char == '.':
                    print("Error: '.' cannot be component character.")
                    quit(1)

                comp.height += 1             # increment the height by 1 as we see the char on prev line 
                components[char] = comp      # update value in component dict

        # creating the adjacency list
        for var in variables:
            adjacency_list[var] = []
            for var2 in variables:
                if var != var2:
                    adjacency_list[var].append(var2)

        file.close()
        return (adjacency_list, domain_list, components, board)


    # the function to call to solve the problem
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

        print(readable)
        
        # getting the locations
        grid = {}
        for char in readable:
            location = readable[char]
            component = self.components[char]

            for x in range(location[0], location[0]+component.length):
                for y in range(location[1], location[1]+component.height):
                    key = str((x, y))
                    grid[key] = char
        
        # printing the circuit board solution
        for r in range(self.board.height, -1, -1):
            for c in range(self.board.length+1):
                key = str((c, r))
                if key in grid:
                    print(grid[key] + " ", end="")
                else:
                    print(". ", end="")
            print("\n")
            

        # return solution
        print('Found solutions after visiting '+str(self.visited)+' nodes.')


    # checks if potential assignment is consistent
    def is_consistent(self, variable, value, assignment):
        neighbors = self.adjacencyList[variable]
        
        # current domain information
        component = self.components[self.int_to_variable[variable]]
        location = self.int_to_domain[value]

        left = location[0]
        bot = location[1]
        right = left + component.length - 1
        top = bot + component.height - 1

        for neighbor in neighbors:
            if assignment[neighbor] is not None:
                # neighbor information
                neighbor_component = self.components[self.int_to_variable[neighbor]]
                neighbor_location = self.int_to_domain[assignment[neighbor]]

                n_left = neighbor_location[0]
                n_bot = neighbor_location[1]
                n_right = n_left + neighbor_component.length - 1
                n_top = n_bot + neighbor_component.height - 1

                # overlapping components
                if left <= n_right and n_left <= right and bot <= n_top and n_bot <= top:
                    return False

                # if the bottom left corner is inside the board, but the rest of the component is outside it
                if right > self.board.length or top > self.board.height:
                    return False

        # if the bottom left corner is inside the board, but the rest of the component is outside it
        if right > self.board.length or top > self.board.height:
            return False
        return True


    # checks if pair in arc consistency method is consistent
    def pair_consistent(self, var1, var2, val1, val2):
        # var1 information
        component = self.components[self.int_to_variable[var1]]
        location = self.int_to_domain[val1]
        left = location[0]
        bot = location[1]
        right = left + component.length - 1
        top = bot + component.height - 1


        # var2 information
        neighbor_component = self.components[self.int_to_variable[var2]]
        neighbor_location = self.int_to_domain[val2]
        n_left = neighbor_location[0]
        n_bot = neighbor_location[1]
        n_right = n_left + neighbor_component.length - 1
        n_top = n_bot + neighbor_component.height - 1

        # if they overlap
        if left <= n_right and n_left <= right and bot <= n_top and n_bot <= top:
            return False

        # if the bottom left corner is inside the board, but the rest of the component is outside it
        if right > self.board.length or top > self.board.height:
            return False

        if n_right > self.board.length or n_top > self.board.height:
            return False
        
        return True
