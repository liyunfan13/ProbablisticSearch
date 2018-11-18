import numpy as np
import random
from generate import generate

flat = 1
hilly = 2
forested = 3
caves = 4

def query(x,y,targetx,targety,terrain):
    print(x,y,targetx,targety,terrain)
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
        factor = 0.9
    elif map[x][y] == hilly:
        factor = 0.7
    elif map[x][y] == forested:
        factor = 0.3
    else:
        factor = 0.1

    temp = beliefmap[x][y]
    #searchedcell = temp*factor
    delta = temp * (1.0-factor)
    dim = map.shape[0]
    for i in range(dim):
        for j in range(dim):
            beliefmap[i][j] += beliefmap[i][j]/(1.0-temp)*delta

    beliefmap[x][y] = temp * factor
    return


def probablisticSearch(map, targetx, targety):
    print(targetx, targety)
    #initialize belief map
    dim = map.shape[0]
    initbelief = 1.0/(dim*dim)
    beliefmap = np.full((dim, dim),initbelief)

    while True:

        # decide which cell to query
        query_i = 0
        query_j = 0
        maxbelief = 0
        for i in range(dim):
            for j in range(dim):
                if beliefmap[i][j] > maxbelief:
                    maxbelief = beliefmap[i][j]
                    query_i = i
                    query_j = j

        query_result = query(query_i,query_j,targetx,targety,map[targetx][targety])
        print(query_result)
        if query_result == 1:
            print("Target found at [%s,%s]."%(query_i,query_j))
            return
        else:
            print("Search [%d,%d]" % (query_i,query_j))
            makeMove(map,beliefmap,query_i,query_j)
        print(beliefmap)
        #return



if __name__ == '__main__':
    game = generate(5)
    map = game.get('board')
    target_x = game.get('target').row
    target_y = game.get('target').col
    probablisticSearch(map,target_x,target_y)

