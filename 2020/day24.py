from collections import defaultdict
TEST = False
DEBUG = False
inp = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew\
"""
with open("day24.input") as f:
    realinp = f.read()
inp: str = realinp if not TEST else inp


def splitinput(inp: str):
    # Strip newlines
    stripped = inp.replace("\n", "").strip()
    out = []
    i = 0
    while i < len(stripped):
        if stripped[i] in ["e", "w"]:
            out += [stripped[i]]
            i += 1
            continue
        out += [stripped[i:i+2]]
        i += 2
    return out

def walk(path: str) -> Tuple[int, int]:
    n,e = 0, 0
    for dir in splitinput(path):
        if dir == "e":
            e += 2
        if dir == "se":
            n -= 1
            e += 1
        if dir == "sw":
            n -= 1
            e -= 1
        if dir == "w":
            e -= 2
        if dir == "nw":
            n += 1
            e -= 1
        if dir == "ne":
            n += 1
            e += 1
    return n, e

assert walk("nwswnwsw") == walk("swnwswnw")
assert walk("nwswnwsw") == walk("ww")
assert walk("enwwswseene") == walk("e")
assert walk("nwwswee") == (0,0)

# Part 1
tiles = defaultdict (bool)
for l in inp.splitlines():
    n, e = walk(l)
    if DEBUG: print(n,e, l)
    tiles[(n, e)] = not tiles[(n,e)]

blacks = sum([1 for t in tiles.values() if t])
print(blacks)

# Part2
# Any black tile with zero or more than 2 black tiles immediately adjacent to
# it is flipped to white.
# Any white tile with exactly 2 black tiles immediately adjacent to it is
# flipped to black.
for d in range(100):
    # Get a count of black neighbors
    # Use this to adjust real-estate pricing
    tilecounts = defaultdict(int)
    for ((n,e), b) in tiles.items():
        # Right now we're only counting blacks
        if not b:
            continue
        tilecounts[(n,e)] += 0
        for dn, de in [(0,2), (-1, 1), (-1, -1), (0, -2), (1, -1), (1,1)]:
            tilecounts[(n+dn, e+de)] += 1
    bcount = 0
    for ((n,e), c) in tilecounts.items():
        if not tiles[(n,e)]:
            if c == 2:
                tiles[(n,e)] = True
                bcount += 1
            continue
        if c == 0 or c > 2:
            tiles[(n,e)] = False
            continue
        bcount += 1

    if DEBUG: print(f"Day {d}, blacks: {bcount}")
print(bcount)



