from collections import defaultdict
from pprint import pprint
import re

prod = True
inp = '''\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
'''

if prod:
    with open("input") as f:
        inp = f.read()

schems = inp.split("\n\n")

locks, keys = [], []
for schem in schems:
    s = schem.split("\n")
    heights = []
    for c in range(5):
        heights.append(len(t := [s[r][c] for r in range(7) if s[r][c] == "#"]) - 1)

    if all([c == "#" for c in s[0]]):
        locks.append(heights)
    else:
        keys.append(heights)
if not prod:
    pprint('locks')
    pprint(locks)
    pprint('keys')
    pprint(keys)

fits = list()
for l in locks:
    for k in keys:
        if all([l[i] + k[i] < 6 for i in range(5)]):
            #print("FIT:", l, k)
            fits.append((l, k))
print(len(fits))
