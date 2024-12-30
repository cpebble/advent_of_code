from math import inf
import re
from functools import cache


prod = True
inp = """\
029A
980A
179A
456A
379A
"""

with open('input') as f:
    if prod:
        inp = f.read()
inp = inp.rstrip()

inp = inp.split("\n")

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
numpadlayout = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"],
                ["X", "0", "A"]]
numpadmap = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3)
}


def numpad(start, end):
    startx, starty = numpadmap[start]
    endx, endy = numpadmap[end]
    movex = endx - startx
    movey = endy - starty
    xchar = ">"
    if movex < 0:
        xchar = "<"
    ychar = "v"
    if movey < 0:
        ychar = "^"
    if startx + movex == 0 and starty == 3:
        # Move vertically first
        return ychar * abs(movey) + xchar * abs(movex) + "A"
    else:
        return xchar * abs(movex) + ychar * abs(movey) + "A"

def sign(x):
    if x > 0:
        return 1
    return -1

def allnumpad(start, end):
    startx, starty = numpadmap[start]
    endx, endy = numpadmap[end]
    movex = endx - startx
    movey = endy - starty
    if movex == 0 and movey == 0:
        return ["A"]
    xchar = ">"
    if movex < 0:
        xchar = "<"
    ychar = "v"
    if movey < 0:
        ychar = "^"
    possibilities = []
    # We either move in the x dir or the y dir
    if movex != 0:
        x = startx + sign(movex)
        if not (starty == 3 and x == 0):
            subpossibilities = allnumpad(numpadlayout[starty][x], end)
            possibilities += [xchar + spos for spos in subpossibilities]
    if movey != 0:
        y = starty + sign(movey)
        if not (y == 3 and startx == 0):
            subpossibilities = allnumpad(numpadlayout[y][startx], end)
            possibilities += [ychar + spos for spos in subpossibilities]

    return possibilities
print(allnumpad("4", "A"))
arrowkeylayout = [["X", "^", "A"], ["<", "v", ">"]]
arrowkeymap = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}

@cache
def arrowkeys(start, end):
    startx, starty = arrowkeymap[start]
    endx, endy = arrowkeymap[end]
    movex = endx - startx
    movey = endy - starty
    xchar = ">"
    if movex < 0:
        xchar = "<"
    ychar = "v"
    if movey < 0:
        ychar = "^"
    if startx + movex == 0 and starty == 0:
        # Move vertically first
        return ychar * abs(movey) + xchar * abs(movex) + "A"
    else:
        return xchar * abs(movex) + ychar * abs(movey) + "A"

@cache
def allarrowkeys(start, end):
    startx, starty = arrowkeymap[start]
    endx, endy = arrowkeymap[end]
    movex = endx - startx
    movey = endy - starty
    if movex == 0 and movey == 0:
        return ["A"]
    xchar = ">"
    if movex < 0:
        xchar = "<"
    ychar = "v"
    if movey < 0:
        ychar = "^"
    possibilities = []
    # We either move in the x dir or the y dir
    if movex != 0:
        x = startx + sign(movex)
        if not (starty == 0 and x == 0):
            subpossibilities = allarrowkeys(arrowkeylayout[starty][x], end)
            possibilities += [xchar + spos for spos in subpossibilities]
    if movey != 0:
        y = starty + sign(movey)
        if not (y == 0 and startx == 0):
            subpossibilities = allarrowkeys(arrowkeylayout[y][startx], end)
            possibilities += [ychar + spos for spos in subpossibilities]

    return possibilities


@cache
def allarrowkeys_(start, end):
    startx, starty = arrowkeymap[start]
    endx, endy = arrowkeymap[end]
    movex = endx - startx
    movey = endy - starty
    xchar = ">"
    if movex < 0:
        xchar = "<"
    ychar = "v"
    if movey < 0:
        ychar = "^"
    if startx + movex == 0 and starty == 0:
        # Move vertically first
        return [ychar * abs(movey) + xchar * abs(movex) + "A"]
    else:
        return [xchar * abs(movex) + ychar * abs(movey) + "A", ychar * abs(movey) + xchar * abs(movex) + "A"]


prevs = ["A", "A", "A"]

#out = ""
#for g1 in "029A":
    #numpgoal = numpad(prevs[2], g1)
    #for g2 in numpgoal:
        #arkgoal = arrowkeys(prevs[1], g2)
        #for g3 in arkgoal:
            #out += arrowkeys(prevs[0], g3)
            #prevs[0] = g3
        #prevs[1] = g2
    #prevs[2] = g1
#print(out)

targets = {
    "029A":
    len("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
        ),
    "980A":
    len("<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A"),
    "179A":
    len("<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
        ),
    "456A":
    len("<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"),
    "379A":
    len("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")
}
def printtarget(target):
    out = ""
    for g1 in target:
        numpgoal = numpad(prevs[2], g1)
        for g2 in numpgoal:
            arkgoal = arrowkeys(prevs[1], g2)
            for g3 in arkgoal:
                out += arrowkeys(prevs[0], g3)
                prevs[0] = g3
            prevs[1] = g2
        prevs[2] = g1
    return out

@cache
def deeptargetstr(prev, target, level=0):
    #print("! ", level, target)
    if level == 0:
        return target
    out = ""
    p = prev
    for g in target:
        goal = arrowkeys(p, g)
        p2 = "A"
        for g2 in goal:
            out += deeptargetstr(p2, g2, level - 1)
            p2 = g2
        p = g
    return out

@cache
def deeptarget(prev, target, level=0, npad=False):
    assert(len(target) == 1)
    if level == 0:
        return 1
    curh = inf
    if npad:
        goals = allnumpad(prev, target)
    else:
        goals = allarrowkeys(prev, target)
    for goal in goals:
        p2 = "A"
        c = 0
        for g2 in goal:
            c += deeptarget(p2, g2, level - 1)
            p2 = g2
        if c < curh:
            curh = c
    return curh
p1 = 0
for l in inp:
    d = int(l[:-1])
    out = 0
    prev = "A"
    for c in l:
        out += (deeptarget(prev, c, 3, npad=True))
        prev = c
    p1 += d*(out)
print(p1)
assert(p1 == 197560)
p2 = 0
for l in inp:
    d = int(l[:-1])
    out = 0
    prev = "A"
    for c in l:
        out += (deeptarget(prev, c, 26, npad=True))
        prev = c
    p2 += d*(out)
print(p2)
assert(p2 < 277554934879758)
assert(p2 < 267879181056862)
assert(p2 > 209424568962722)

#v<<A>>^A<A>AvA<^AA>A<vAAA>^A
#v<<AA<AAvA<A<AA<vA<vA<vAA


