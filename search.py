import numpy as np
import random
from generate import generate

flat = 1
hilly = 2
forested = 3
caves = 4

def query(x,y,targetx,targety,terrain):
    #print("trying [%s,%s]" % (x,y))
    if x==targetx and y==targety:
        seed = random.random()
        if terrain == flat:
            if seed < 0.1:
                return 0
            else:
                return 1
        if terrain == hilly:
            if seed < 0.3:
                return 0
            else:
                return 1
        if terrain == forested:
            if seed < 0.7:
                return 0
            else:
                return 1
        if terrain == caves:
            if seed < 0.9:
                return 0
            else:
                return 1
    else:
        return 0





def makeMove(map, beliefmap, x, y):

    # update belief map
    factor = 0.0
    if map[x][y] == flat:
        factor = 0.1
    elif map[x][y] == hilly:
        factor = 0.3
    elif map[x][y] == forested:
        factor = 0.7
    else:
        factor = 0.9

    temp = beliefmap[x][y]
    #searchedcell = temp*factor
    delta = temp * (1.0-factor)
    dim = map.shape[0]
    for i in range(dim):
        for j in range(dim):
            beliefmap[i][j] += beliefmap[i][j]/(1.0-temp)*delta

    beliefmap[x][y] = temp * factor
    # regularization
    sum = 0
    for i in range(dim):
        for j in range(dim):
            sum += beliefmap[i][j]

    for u in range(dim):
        for v in range(dim):
            beliefmap[u][v] = beliefmap[u][v] / sum

    #print(beliefmap)
    return


def probablisticSearch(map, targetx, targety, policy):
    #print(targetx, targety)
    #initialize belief map
    dim = map.shape[0]
    initbelief = 1.0/(dim*dim)
    beliefmap = np.full((dim, dim),initbelief)
    count = 0
    while True:
        count+=1
        # decide which cell to query
        maxbelief = 0

        maxcells = []


        if policy == 1:  # highest prob of containing the target
            for i in range(dim):
                for j in range(dim):
                    if beliefmap[i][j] > maxbelief:
                        maxbelief = beliefmap[i][j]
                        maxcells.clear()
                        maxcells.append((i,j,beliefmap[i][j]))
                    elif beliefmap[i][j] == maxbelief:
                        maxcells.append((i,j,beliefmap[i][j]))
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
                        maxcells.append((i,j,beliefmap[i][j]))
                    elif beliefmap[i][j]*p == maxbelief:
                        maxcells.append((i,j,beliefmap[i][j]))


        #break ties arbitrarily
        seed = random.random()
        query_cell_index = int(seed*(len(maxcells)-1))
        query_i = maxcells[query_cell_index][0]
        query_j = maxcells[query_cell_index][1]


        query_result = query(query_i,query_j,targetx,targety,map[targetx][targety])
        #print(query_result)
        if query_result == 1:
            print("Target found at [%s,%s], %s."%(query_i,query_j,map[query_i][query_j]))
            print("Totoal Search Steps:%d" % count)
            return count
        else:
            #print("Search [%d,%d]" % (query_i,query_j))
            makeMove(map,beliefmap,query_i,query_j)
            for i in range(dim):
                for j in range(dim):
                    if beliefmap[i][j] < 0:
                        raise Exception("ERROR")
                        #return count






if __name__ == '__main__':
    game = generate(50)
    map = game.get('board')
    target_x = game.get('target').row
    target_y = game.get('target').col

    # map = np.array([[1,2,3,4],
    #                 [4,3,2,1],
    #                 [1,3,2,4],
    #                 [4,2,3,1]])
    # target_x = 0
    # target_y = 3

    searchstep1 = 0
    searchstep2 = 0
    policy = 1
    for i in range(100):
        steps = probablisticSearch(map,target_x,target_y, 1)
        searchstep1 += steps
        print(steps)

    for i in range(100):
        steps = probablisticSearch(map, target_x, target_y, 2)
        searchstep2 += steps
        print(steps)

    average1 = searchstep1 / 100
    print("Average search step for Rule 1: %d" % average1)
    average2 = searchstep2 / 100
    print("Average search step for Rule 2: %d" % average2)

