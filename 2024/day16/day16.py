from collections import defaultdict
from pprint import pprint
from queue import PriorityQueue
from math import inf

prod = True
inp = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

inp2 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""
inp = inp2
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

#dir = 1
scores = defaultdict(lambda: inf)
wq = PriorityQueue()
wq.put((0, sx, sy, 1, []))
bestpaths = []
while wq.qsize() > 0:
    s, x, y, dir, bp = wq.get(timeout=1)
    scores[(x, y, dir)] = min(scores[(x, y, dir)], s)
    if scores[(x, y, dir)] < s:
        continue
    if x == ex and y == ey and s == min(
        [scores[x, y, 0], scores[x, y, 1], scores[x, y, 2], scores[x, y, 3]]):
        print(s)
        bestpaths.append((s, bp))
        continue
    p = bp + [(x, y)]
    dy, dx = dirs[dir]
    if isallowed(x + dx, y + dy):
        wq.put((s + 1, x + dx, y + dy, dir, p))
    ld, rd = (dir - 1) % 4, (dir + 1) % 4
    dy, dx = dirs[ld]
    if isallowed(x + dx, y + dy):
        wq.put((s + 1001, x + dx, y + dy, ld, p))
    dy, dx = dirs[rd]
    if isallowed(x + dx, y + dy):
        wq.put((s + 1001, x + dx, y + dy, rd, p))
print("Done", len(bestpaths))
p = set()
for path in bestpaths:
    p = p.union(set(path[1]))
#pprint(bestpaths)
for (x, y) in p:
    inp[y][x] = "O"
for r in range(h):
    for c in range(w):
        print(inp[r][c], end="")
    print()

print(len(p)+1)
