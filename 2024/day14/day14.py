import re
import sys
from collections import Counter

prod = True
inp = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

with open("input") as f:
    if prod:
        inp = f.read()
        inp.strip()
inp = inp.split("\n")

if prod:
    h, w = 103, 101
else:
    h, w = 7, 11

robots = []
for line in inp:
    if len(line) < 2:
        print(line)
        continue
    p, v = re.findall(r"(-?\d*),(-?\d*)", line)
    robots.append(((int(p[0]), int(p[1])), (int(v[0]), int(v[1]))))

#robots_after = []
#for p, v in robots:
    #x, y = p
    #dx, dy = v
    #for t in range(100):
        #x = (x + dx) % w
        #y = (y + dy) % h
    #robots_after.append((x, y))
#print(list(sorted(robots_after, key=lambda n: n[0])))
# 5293
for t in range(10000):
    picture = []
    for i in range(h):
        picture += [(["."]*w)]

    for i, (p, v) in enumerate(robots):
        x, y = p
        dx, dy = v
        x = (x + dx) % w
        y = (y + dy) % h
        robots[i] = ((x, y), (dx, dy))
        picture[y][x] = "@"
    c = Counter()
    for (x, y), _ in robots:
        c[x] += 1

    shouldcontinue = True
    for x in c:
        if c[x] > 25:
            shouldcontinue = False
    if shouldcontinue: # and not t % 100 == 0:
        continue
    for line in picture:
        print("".join(line))
    print("Is christmas tree? " + str(t))
    if True and input() == "y":
        print(t)
        sys.exit(0)
#print(list(sorted(robots_after, key=lambda n: n[0])))

xmid = w // 2
ymid = h // 2

quads = [[0, 0], [0, 0]]
for (x, y), (_, _) in robots:
    if x < xmid:
        qx = 0
    elif x > xmid:
        qx = 1
    else:
        continue
    if y < ymid:
        qy = 0
    elif y > ymid:
        qy = 1
    else:
        continue
    quads[qx][qy] += 1
print(quads)
print(quads[0][0] * quads[0][1] * quads[1][0] * quads[1][1])

#......2..1.
#...........
#1..........
#.11........
#.....1.....
#...12......
#.1....1....
#
#......@..@.
#...........
#@..........
#.@@........
#.....@.....
#...@@......
#.@....@....
