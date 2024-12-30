from collections import defaultdict, Counter
from pprint import pprint
from queue import PriorityQueue
from math import inf


prod = True
inp = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

with open('input') as f:
    if prod:
        inp = f.read()
inp = inp.rstrip()

inp = inp.split("\n")
sx, sy = (0, 0)
ex, ey = (0, 0)
for i, r in enumerate(inp):
    if "E" in r:
        ey, ex = (i, r.index("E"))
    if "S" in r:
        sy, sx = (i, r.index("S"))
inp = list(map(list, inp))
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

w, h = (len(inp[0]), len(inp))

iswithin = lambda x, y: x >= 0 and x < w and y >= 0 and y < h
isallowed = lambda x, y: iswithin(x, y) and inp[y][x] != "#"

# Get a list of scores
scores = defaultdict(lambda: inf)
wq = PriorityQueue()
wq.put((0, sx, sy))
bestpaths = []
while wq.qsize() > 0:
    s, x, y = wq.get(timeout=1)
    if scores[(x, y)] <= s:
        continue
    scores[(x, y)] = s
    for dir in range(4):
        dy, dx = dirs[dir]
        if isallowed(x + dx, y + dy):
            wq.put((s + 1, x + dx, y + dy))
print("Made score map")
print("Race is winnable in:", scores[(ex, ey)])

nodes = set()
nodes.add((sx, sy))
cheats = Counter()
# I don't need two loops, however the nesting beomes fugly
for y in range(h):
    for x in range(w):
        if inp[y][x] == ".":
            nodes.add((x, y))
for (x, y) in nodes:
    s = scores[(x, y)]
    # Take two steps
    for dy, dx in dirs:
        for dy_, dx_ in dirs:
            ny = y + dy + dy_
            nx = x + dx + dx_
            if isallowed(nx, ny):
                ns = scores[(nx, ny)]
                if ns > s + 2:
                    cheats[ns - (s + 2)] += 1
p1 = 0
for (e, c) in cheats.items():
    if e >= 100:
        p1 += c
print("Part1:", p1)
del cheats
cheats = Counter()
dirs2 = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
cc = set()
for (x, y) in nodes:
    s = scores[(x, y)]
    for dx in range(21):
        for dy_ in range(-1, 20-dx):
            dy = dy_ + 1
            dist = dx + dy
            #print(f"Stepping {dx + dy}({dx, dy}")
            for fx, fy in dirs2:
                nx = x + (dx*fx)
                ny = y + (dy*fy)
                if (x, y, nx, ny) in cc:
                    continue
                if scores[(nx, ny)] == inf:
                    continue
                if scores[(nx, ny)] <= s:
                    continue
                diff = scores[(nx, ny)] - (s + dist)
                if diff > dist:
                    cc.add((x, y, nx, ny))
                    cheats[diff] += 1
part2 = 0
for c in sorted(cheats.keys()):
    if c >= 100:
        print(f"There are {cheats[c]} cheats that save {c} picoseconds.")
        part2 += cheats[c]
print(len(cheats))
print(part2)
