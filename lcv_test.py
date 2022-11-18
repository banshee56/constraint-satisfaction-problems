# file to test lcv heuristic

possDict = {}
possDict[0] = [1, 2, 9, 6]
possDict[1] = [2, 3, 4, 6]
possDict[2] = [12, 18, 19, 20, 6]
int_to_char = {0: 'A', 1: 'B', 2: 'C'}
assignment = [None, None, None]
adj_list = {0: [1, 2], 1: [0], 2: [0]}


# possDict = {}
# possDict[0] = [1, 2, 4]
# possDict[1] = [2, 3]
# int_to_char = {0: 'A', 1: 'B'}
# assignment = [None, None]
# adj_list = {0: [1, 2], 1: [0]}

def minimum_remaining_values(assignment):
    min_moves = float('inf')

    for key in possDict:
        # if this key already has an assignment
        if assignment[key] is not None:
            continue

        possible_values = possDict[key]

        if len(possible_values) < min_moves:
            mrv = []                            # start list from scratch whenever we find a better mrv candidate
            min_moves = len(possible_values)
            mrv.append(key)
        
        # ties for degree heuristic to handle
        elif len(possible_values) == min_moves: # if this move is tied with the current mrv candidate
            mrv.append(key)                     # put them in together

    # # if not paired with degree heuristic, just send one of the tied variables as answer
    # if not self.dh:
    return mrv

def select_unassigned_variable(assignment):
    mrv = []

    mrv = minimum_remaining_values(assignment)

    # if dh turned off but mrv turned on then just return the first (tied) mrv
    return mrv[0]

def least_constraining_value(variable, assignment):
        lcv = {}

        for domain in possDict[variable]:
            changed = reduce_possibilities(variable, domain, assignment)
            # neighbors post-reduction
            neighbors = adj_list[variable]
            sum = 0
            for neighbor in neighbors:
                sum += len(possDict[neighbor])
            
            lcv[domain] = sum
            increase_possibilities(variable, domain, assignment, changed)

        # print(lcv)
        # sort the dict by the values (sums) and then add the keys (domains) to the domain list
        sortedLCV = sorted(lcv, key=lcv.get, reverse=True)
    
        return sortedLCV

def order_domain_values(variable, assignment):
        domainList = []   
        domainList = least_constraining_value(variable, assignment)
        return domainList

def reduce_possibilities(variable, value, assignment):
        neighbors = adj_list[variable]
        changed = []
        
        for neighbor in neighbors:
            # go through all the neighbors of the variable and remove this value from its possible values
            if assignment[neighbor] is None and value in possDict[neighbor]:
                possDict[neighbor].remove(value)
                changed.append(neighbor)
        
        return changed
        # we would remove all other values from the possibility list for the current variable
        # but mrv does not even consider the possibilities of variables that are already assigned
        # so no need to change the possibilities here, it would just add extra work having to add them back later in increase_possibilities

# undo everything done above
def increase_possibilities(variable, value, assignment, changed):
    neighbors = adj_list[variable]
    for neighbor in neighbors:

        # go through all the unassigned neighbors of the variable and add this value to its possible values
        if assignment[neighbor] is None and neighbor in changed:
            possDict[neighbor].append(value)

mrv = select_unassigned_variable(assignment)
print(int_to_char[mrv])

dom = order_domain_values(mrv, assignment)
print(dom)