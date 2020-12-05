from collections import Counter

c = Counter()

testwires = [
    ["R75","D30","R83","U83","L12","D49","R71","U7","L72"],
    ["U62","R66","U55","R34","D71","R55","D58","R83"]
]

wires = []
with open("day3.input") as f:
    for line in f:
        wires += [line.split(',')]


directions = {
        "U": (0,1),
        "R": (1,0),
        "D": (0,-1),
        "L": (-1,0),
}

def parseStep(ins):
    direction = directions[ins[0]]
    distance = int(ins[1:])
    return direction, distance

def walk(wire, startpos):
    global c
    pos = startpos
    for instruction in wire:
        direction, distance = parseStep(instruction)
        for i in range(distance):
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            c[pos] += 1

if __name__ == "__main__":
    path = {}
    intersections = []
    # Calculate first wire
    wire = wires
    pos = (0,0)
    leng = 0
    for ins in wire[0]:
        direction, distance = parseStep(ins)
        for i in range(distance):
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            leng += 1
            if pos not in path:
                path[pos] = leng
            elif path[pos] > leng: # Unneccesary
                path[pos] = leng
    pos = (0,0)
    leng = 0
    for ins in wire[1]:
        direction, distance = parseStep(ins)
        for i in range(distance):
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            leng += 1
            if pos in path:
                #path[pos]
                intersections += [(pos, leng)]

    minima = 9999
    for pos, b in intersections:
        a = path[pos]
        d = a + b
        if minima > d:
            minima = d
    print(minima)
