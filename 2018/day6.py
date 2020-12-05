import pickle
import threading
from collections import Counter
from math import floor


def calcPoint(x, y):
    minId = str(-1)
    minCost = bw+bh
    for p in points:
        distanceX = abs(p[0]-x)
        distanceY = abs(p[1]-y)
        cost = distanceX + distanceY
        if cost < minCost:
            minCost = cost
            minId = str(p[2])
        elif cost == minCost:
            minId = str(".")

    return (minId, minCost)


def calcClose(x, y):
    maxDis = 10_000
    disSum = 0
    for p in points:
        distanceX = abs(p[0]-x)
        distanceY = abs(p[1]-y)
        cost = distanceX + distanceY
        disSum += cost
    if disSum < maxDis:
        return (True, disSum)
    else:
        return (False, disSum)


if __name__ == "__main__":
    points = []
    with open("day6.input") as inp:
        i = 1
        maxX = 0
        maxY = 0
        for line in inp:
            x, y = line.split(",")
            points += [(int(x), int(y), str(i))]
            i += 1
            maxX = max([maxX, int(x)])
            maxY = max([maxY, int(y)])
    # maxX = 10
    # maxY = 10
    bw, bh = (floor(maxX+20), floor(maxY+20))
    board = [[] for y in range(bh)]
    for y in range(bh):
        board[y] = [calcPoint(x, y) for x in range(bw)]

    # for x in range(len(board)):
    #     for y in range(len(board[x])):
    #         board[x][y] = calcPoint(x, y)

    infSet = set()
    for i in range(bw):
        infSet.add(board[0][i][0])
        infSet.add(board[bh-1][i][0])
    for i in range(bh):
        infSet.add(board[i][0][0])
        infSet.add(board[i][bw-1][0])
    counter = Counter()
    for y in range(bh):
        for x in range(bw):
            p = board[y][x]
            if p[0] in infSet:
                continue
            counter[p[0]] += 1
    print(counter.most_common())
    # for y in range(bh):
    #     for x in range(bw):
    #         print(board[y][x][0], end="")
    # print()
    board = [[] for y in range(bh)]
    closeReg = 0
    for y in range(bh):
        for x in range(bw):
            isclose, distance = calcClose(x, y)
            if isclose:
                closeReg += 1
    print(closeReg)
