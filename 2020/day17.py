
import pdb
from collections import defaultdict
TEST = True
test = """\
.#.
..#
###\
"""

with open("day17.input") as f:
    realin = f.read()

initial = realin if TEST else test

state = set()

# Parse input
z = 0
rows = initial.splitlines()
for y in range(len(rows)):
    for x in range(len(rows[y])):
        if rows[y][x] == "#":
            state.add((x, y, z))

def printState(st):
    maxX = max(st, key=lambda c: c[0])[0]
    maxY = max(st, key=lambda c: c[1])[1]
    maxZ = max(st, key=lambda c: c[2])[2]
    minX = min(st, key=lambda c: c[0])[0]
    minY = min(st, key=lambda c: c[1])[1]
    minZ = min(st, key=lambda c: c[2])[2]
    for z in range(minZ, maxZ+1):
        print(f"Z={z}")
        grid = ""
        for y in range(minY, maxY+1):
            l = ""
            for x in range(minX, maxX+1):
                l += "#" if (x,y,z) in st else "." 
            grid += f"\n{l}"
        print(grid + "\n")
    print("")

def step(state: set) -> set:
    next = defaultdict(int)
    for (x,y,z) in state:
        for (dx,dy,dz) in [(dx,dy,dz) for dx in [-1,0,1] for dy in [-1, 0, 1] for dz in [-1, 0, 1] if (dx,dy,dz) != (0,0,0)]:
            next[(x+dx, y+dy, z+dz)] += 1
    rval = set()
    for k,v in next.items():
        if (k in state and (v == 2 or v == 3)) or (not k in state) and v == 3:
            rval.add(k)

    return rval
def lift(state: set):
    return set([(x,y,z,0) for (x,y,z) in state])
def step2(state: set) -> set:
    next = defaultdict(int)
    for (x,y,z,w) in state:
        for (dx,dy,dz,dw) in [(dx,dy,dz,dw) 
                for dx in [-1,0,1] 
                for dy in [-1, 0, 1] 
                for dz in [-1, 0, 1] 
                for dw in [-1, 0, 1] 
                if (dx,dy,dz,dw) != (0,0,0,0)]:
            next[(x+dx, y+dy, z+dz, w+dw)] += 1
    rval = set()
    for k,v in next.items():
        if (k in state and (v == 2 or v == 3)) or (not k in state) and v == 3:
            rval.add(k)

    return rval

print(len(step(step(step(step(step(step(state))))))))
print(len(step2(step2(step2(step2(step2(step2(lift(state)))))))))

