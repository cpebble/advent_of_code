from collections import defaultdict
from itertools import combinations, permutations
prod = True

inp = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............\
""".split("\n")
with open('input') as f:
    if prod: 
        inp = f.readlines()

inp = list(map(lambda s: list(s.strip()), inp))
h, w = len(inp), len(inp[0])

antennas = defaultdict(list)

for r in range(h):
    for c in range(w):
        if inp[r][c] != ".":
            antennas[inp[r][c]].append((r, c))
#print(antennas)

antinodes = set()
for freq in antennas:
    for (a, b) in permutations(antennas[freq], 2):
        (ar, ac) = a
        (br, bc) = b
        # Antinode 1
        n1r = br + (br - ar)
        n1c = bc + (bc - ac)
        if n1r >= 0 and n1r < h and n1c >= 0 and n1c < w:
            antinodes.add((n1r, n1c))

print(len(antinodes))
#print("\n".join(list(map("".join, inp))))
print(len(inp[0]), w)
resantinodes = set()
for freq in antennas:
    for (a, b) in permutations(antennas[freq], 2):
        (ar, ac) = a
        (br, bc) = b
        dr = br - ar
        dc = bc - ac
        i = 0
        while True:
            # Antinode
            n1r = br + (dr*i)
            n1c = bc + (dc*i)
            if n1r >= 0 and n1r < h and n1c >= 0 and n1c < w:
                resantinodes.add((n1r, n1c))
                i += 1
            else:
                break

print(len(resantinodes))
