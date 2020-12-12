instr = open("day12.input").readlines()

pos = [0, 0]
rot = 0
dirs = {
        "N": (1, 0),
        "S": (-1, 0),
        "E": (0, 1),
        "W": (0, -1)
    }
rots = ["E", "N", "W", "S"]

def parseIns(pos, rot, i, n):
    npos = pos
    nrot = rot
    if i in dirs:
        y, x = pos
        dy, dx = dirs[i]
        ny, nx = (dy*n + y , dx*n + x)
        npos = (ny, nx)
        #print(f"Moving from {
    elif i == "L":
        if n % 90 != 0:
            print("unsafe turning angle")
        dr = n // 90
        nrot = (rot + dr) % 4;
    elif i == "R":
        if n % 90 != 0:
            print("unsafe turning angle")
        dr = n // 90
        nrot = (rot - dr) % 4;
    elif i == "F":
        return parseIns(pos, rot, rots[rot], n)
    return (npos, nrot)

for (i, n) in [(x[0], int(x[1:].strip())) for x in instr]:
    pos, rot = parseIns(pos, rot, i, n)
    print(i, n, pos, rot)
print(abs(pos[0]) + abs(pos[1]))

# Part 2

pos = (0, 0)
wayp= (1, 10)

for (i, n) in [(x[0], int(x[1:].strip())) for x in instr]:
    npos = pos
    nrot = rot
    if i in dirs:
        y, x = wayp
        dy, dx = dirs[i]
        ny, nx = (dy*n + y , dx*n + x)
        wayp = (ny, nx)
        #print(f"Moving from {
    elif i == "L":
        for _ in range(n // 90):
            wy, wx = wayp
            wayp = (wx, -wy)
    elif i == "R":
        for _ in range(n // 90):
            wy, wx = wayp
            wayp = (-wx, wy)
    elif i == "F":
        y,x = pos
        dy,dx = wayp
        #dy = wy + y
        #dx = wx + x
        #print(dy, dx, "Moving", dy*n, dx*n)
        pos = (y + dy*n,x + dx*n)
    print(pos, wayp)

print(abs(pos[0]) + abs(pos[1]))

