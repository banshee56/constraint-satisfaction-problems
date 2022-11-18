# file to test arc consistency

from collections import deque

def arc_consistency_3():
    global arc_set, adjacencyList, i
    # initialized to all arcs
    queue = deque()
    removedDict = {}

    for pair in arc_set:
        queue.append(pair)

    print(queue)
    while queue:
        pair = queue.popleft()
        x_i = pair[0]
        x_j = pair[1] 

        # if pair is inconsistent and inconsistent domain values were removed
        removed = remove_inconsistent_variables(x_i, x_j, removedDict)

        # if some domain was removed from x_i
        if removed:

            # add the neighbors of x_i to the queue again
            for x_k in adjacencyList[x_i]:
                pair = (x_k, x_i)
                queue.append(pair)
            
            if i < 2:
                print(queue)
                print('------')
                i += 1 
       
    return removedDict


def remove_inconsistent_variables(x_i, x_j, removedDict):
    global possibility_dict, adjacencyList, i
    if i < 2:
        print(possibility_dict)

    removed = False

    for x in possibility_dict[x_i]:

        # if x_j is a neighbor of x_i and the current domain value of x is the only possible domain of x_j
        if x_j in adjacencyList[x_i] and possibility_dict[x_j] == [x]:            
            # remove x from domain of x_i
            if i < 0:
                print(x_i + '-->' + x_j)

            possibility_dict[x_i].remove(x)
            removed = True

            if x_i not in removedDict:
                removedDict[x_i] = []
            if x_i in removedDict:
                removedDict[x_i].append(x)  

    return removed


var = ['bans', 'aps', 'mateo']
adjacencyList = {
                'bans': ['aps', 'mateo'], 
                'aps': ['bans'],
                'mateo': ['bans']
                }
arc_q = set()
# for each variable
for i in var:
    # and for each neighbor of that variable
    for j in adjacencyList[i]:
        # we get a pair of adjacent variables
        pair = (i, j)
        arc_q.add(pair)

i = 0
arc_set = arc_q
possibility_dict = {'bans': [0], 'aps': [1, 2], 'mateo': [0, 1]}
print(arc_consistency_3())