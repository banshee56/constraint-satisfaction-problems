from MapColoringCSP import MapColoringCSP

def get_params(file):
    domain_list = file.readline().strip().split(',')

    adjacency_list = {}
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

    return (adjacency_list, domain_list)

# edit filename for input
file = open('us_states.txt', 'r')
(adjacency_list, domain_list) = get_params(file)


mapColoringProblem = MapColoringCSP(adjacency_list, domain_list)
solution = mapColoringProblem.solve_csp()

if solution:
    print(solution)
