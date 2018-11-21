import numpy as np
import random
from generate import generate
from search import query
from search import makeMove

flat = 1
hilly = 2
forested = 3
caves = 4

def manhattanDistance(x1,y1,x2,y2):
    delta_x = abs(x2-x1)
    delta_y = abs(y2-y1)
    return delta_x+delta_y

def move(x1,y1,x2,y2):

    if x1==x2 and y1==y2:
        return x1,y1
    # horizontal move has higher priority
    if x2>x1:
        return x1+1, y1
    elif x1>x2:
        return x1-1, y1
    elif y2>y1:
        return x1, y1+1
    else:
        return x1, y1-1



def probablisticSearch(map, targetx, targety, policy):
    dim = map.shape[0]
    initbelief = 1.0 / (dim * dim)
    beliefmap = np.full((dim, dim), initbelief)
    count = 0
    search_count = 0
    move_count = 0
    current_i = 0
    current_j = 0

    destination_i = 0
    destination_j = 0

    while True:
        count += 1
        maxbelief = 0
        maxcells = []

        if policy == 1:  # highest prob of containing the target
            for i in range(dim):
                for j in range(dim):
                    if beliefmap[i][j] > maxbelief:
                        maxbelief = beliefmap[i][j]
                        maxcells.clear()
                        maxcells.append((i,j))
                    elif beliefmap[i][j] == maxbelief:
                        maxcells.append((i,j))
        else:             # highest prob of finding the target
            for i in range(dim):
                for j in range(dim):
                    p = 0
                    if map[i][j] == flat:
                        p = 0.9
                    elif map[i][j] == hilly:
                        p = 0.7
                    elif map[i][j] == forested:
                        p = 0.3
                    else:
                        p = 0.1

                    if beliefmap[i][j]*p > maxbelief:
                        maxbelief = beliefmap[i][j]*p
                        maxcells.clear()
                        maxcells.append((i,j))
                    elif beliefmap[i][j]*p == maxbelief:
                        maxcells.append((i,j))

        # break ties arbitrarily
        seed = random.random()
        print(maxcells)
        query_cell_index = int(seed * (len(maxcells) - 1))
        query_i = maxcells[query_cell_index][0]
        query_j = maxcells[query_cell_index][1]

        for cell in maxcells:
            if cell[0] == destination_i and cell[1] == destination_j and count != 1:
                query_i = destination_i
                query_j = destination_j

        print("==========")
        print("Max belief is %s" % maxbelief)
        print("Max belief cell is [%s,%s]" % (query_i,query_j))
        print("Current cell is [%s,%s]" % (current_i,current_j))

        if_search = 1

        # the first search is starting point
        if count == 1 or (current_i==query_i and current_j==query_j):
            print("No need to move")
            current_i = query_i
            current_j = query_j
        else: # decide whether to move or search
            distance = manhattanDistance(current_i,current_j,query_i,query_j)
            print("distance:%s" % distance)
            destination = maxbelief

            for i in range(distance):
                destination = destination*0.95

            if policy == 1:
                if beliefmap[current_i][current_j] < destination:
                    current_i, current_j = move(current_i,current_j,query_i,query_j)
                    print("moving to [%s,%s]" % (current_i,current_j))
                    move_count += 1
                    if_search = 0
            else:
                p = 0
                if map[i][j] == flat:
                    p = 0.9
                elif map[i][j] == hilly:
                    p = 0.7
                elif map[i][j] == forested:
                    p = 0.3
                else:
                    p = 0.1
                if beliefmap[current_i][current_j]*p < destination:
                    current_i, current_j = move(current_i, current_j,query_i,query_j)
                    if_search = 0
        query_result = 0
        if if_search == 1:
            search_count += 1
            query_result = query(current_i, current_j, targetx, targety, map[targetx][targety])
            if query_result == 1:
                print("Target found at [%s,%s]." % (current_i, current_j))
                print("Totoal Search Steps:%d" % search_count)
                return search_count, move_count
            else:
                # print("Search [%d,%d]" % (query_i,query_j))
                makeMove(map, beliefmap, current_i, current_j)
                for i in range(dim):
                    for j in range(dim):
                        if beliefmap[i][j] < 0:
                            raise Exception("ERROR")




if __name__ == '__main__':
    game = generate(5)
    map = game.get('board')
    target_x = game.get('target').row
    target_y = game.get('target').col
    searchstep1 = 0
    searchstep2 = 0
    movestep1 = 0
    movestep2 = 0

    policy = 1
    #for i in range(10):
    searchsteps, movesteps = probablisticSearch(map,target_x,target_y, 1)
        #searchstep1 += searchsteps
        #movestep1 += movesteps
    print(searchsteps, movesteps)

    # for i in range(100):
    #     searchsteps, movesteps = probablisticSearch(map, target_x, target_y, 2)
    #     searchstep2 += searchsteps
    #     movestep2 += movesteps
    #     print(searchsteps,movesteps)

    #average1 = searchstep1 / 10
    #average3 = movestep1 / 10
    #print("Average search step for Rule 1: %d" % average1)
    #print("Average move step for Rule 1: %d" % average3)

    # average2 = searchstep2 /100
    # average4 = movestep2 / 100
    # print("Average search step for Rule 2: %d" % average2)
    # print("Average move step for Rule 2: %d" % average4)






