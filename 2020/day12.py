instr = open("day12.input").readlines()

pos = 0+0j
rot = 0
dirs = {
        "N": 1j,
        "S": -1j,
        "E": 1,
        "W": -1,
    }
rots = ["E", "N", "W", "S"]

def parseIns(pos, rot, i, n):
    npos = pos
    nrot = rot
    if i in dirs:
        print(i)
        npos = pos + (dirs[i] * n)
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
print(int(abs(pos.real) + abs(pos.imag)))
# Part 2

pos = 0+0j
wayp= 10+1j

for (i, n) in [(x[0], int(x[1:].strip())) for x in instr]:
    npos = pos
    nrot = rot
    if i in dirs:
        wayp = wayp + (dirs[i]*n)
    elif i == "L":
        for _ in range(n // 90):
            wayp *= 1j
    elif i == "R":
        for _ in range(n // 90):
            wayp *= -1j
    elif i == "F":
        pos += wayp*n
    print(pos, wayp)

print(int(abs(pos.real) + abs(pos.imag)))
