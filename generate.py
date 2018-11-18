import numpy
import random

class target:
    def __init__(self, dim):
        self.row = int(random.random() * dim)
        self.col = int(random.random() * dim)

    def move(self, dim):
        r = random.random()
        if r < 0.25 and self.row > 0:  #move up
            self.row -= 1
        elif r >= 0.25 and r < 0.5 and self.col + 1 < dim:  #move right
            self.col += 1
        elif r >= 0.5 and r <= 0.75 and self.row + 1 < dim:  #move down
            self.row += 1
        elif r >= 0.75 and r < 1 and self.col > 0:  #move left
            self.col -= 1


def generate(dim):
    # each number represent different landscape
    flat = 1
    hilly = 2
    forested = 3
    caves = 4

    board = numpy.zeros((dim, dim), int)
    for i in range(dim):
        for j in range(dim):
            p = random.random() * 10
            if p > 0 and p < 2:
                board[i][j] = flat
            elif p >= 2 and p < 5:
                board[i][j] = hilly
            elif p >= 5 and p < 8:
                board[i][j] = forested
            else:
                board[i][j] = caves
    t = target(dim)
    d = {'board': board, 'target': t}
    return d

#test
# obj = generate(50)
# board = obj.get('board')
# row = obj.get('target').row
# col = obj.get('target').col
# print(board)
# print(row, col, board[row][col])