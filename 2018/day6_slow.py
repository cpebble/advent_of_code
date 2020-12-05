import os
import queue
import time
from collections import deque
import pickle

bh = 370
bw = 370
board = [(".", 100) for i in range(bh*bw)]
expandQueue = deque()
maxCost = 100


def expand(index, cost, tile):
    (up, down, left, right) = (index+bw, index-bw, index-1, index+1)
    if cost >= maxCost:
        return
    # Check if @ walls
    if index % bw != 0 and board[left][1] >= cost:
        # expand left
        expandQueue.append((left, cost+1, tile))
    if index % bw != bw-1 and board[right][1] >= cost:
        # expand right
        expandQueue.append((right, cost+1, tile))
    if index < bw*(bh-1) and board[up][1] >= cost:
        # expand up
        expandQueue.append((up, cost+1, tile))
    if index > bw and board[down][1] >= cost:
        # expand down
        expandQueue.append((down, cost+1, tile))

    # if cost > 0:
    #     tile = tile.lower()
    if board[index][1] == cost and board[index][0].lower() != tile.lower():
        board[index] = (".", cost)
    elif board[index][1] > cost:
        board[index] = (tile, cost)


def coordsToBoard(x, y):
    assert(x < bw)
    return bh*y + x


def addBlock(x, y, tile):
    expand(coordsToBoard(x, y), 0, tile)
    board[coordsToBoard(x, y)] = (tile, 0)


def printBoard(board):
    os.system("clear")
    for i in range(len(board)):
        # COST: print("{:3d}".format(board[i][1]), end="")
        print(board[i][0], end="")
        # print(" {:2}".format(i), end="")
        if i % bw == (bw):
            print()


if __name__ == "__main__":
    points = []
    with open("day6.input") as inp:
        i = 0
        for line in inp:
            x, y = line.split(",")
            points += [(int(x), int(y), str(i))]

    for x, y, tile in points:
        addBlock(x, y, tile)

    a = 0
    while(len(expandQueue) > 0):
        (index, cost, tile) = expandQueue.popleft()
        expand(index, cost, tile)
        a += 1
        if a % 50 == 0:
            print("Reached count {}, len of queue: {}".format(a, len(expandQueue)))
    print("Did queue")
    with open("out6.bin", "wb") as oout:
        pickle.dump(board, oout)


exampleCoords = [
    (1, 1, "A"),
    (1, 6, "B"),
    (8, 3, "C"),
    (3, 4, "D"),
    (5, 5, "E"),
    (8, 9, "F")
]
if __name__ == "__imain__":
    for (x, y, tile) in exampleCoords:
        addBlock(x, y, tile)

    printBoard(board)
    newCoords = input("Start sim?")
    while(len(expandQueue) > 0):
        (index, cost, tile) = expandQueue.popleft()
        expand(index, cost, tile)

    printBoard(board)
