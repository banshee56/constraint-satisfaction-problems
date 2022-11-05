from MapColoringCSP import MapColoringCSP

file = open('aus_states.txt', 'r')
# variables = file.readline()
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

print(domain_list)
# print(adjacency_list)

mapColoringProblem = MapColoringCSP(adjacency_list, domain_list)

print(mapColoringProblem.solve_csp())