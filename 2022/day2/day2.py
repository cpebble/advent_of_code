


scoreMap = {
    "A": 1,
    "B": 2,
    "C": 3
    }
winMap = {
    "A": "B",
    "B": "C",
    "C": "A"
    }

winScores = [0,3,6]
def calcWin(a,b):
    if b == winMap[a]:
        return 6
    if a == b:
        return 3
    return 0


def genMaps():
    return [{"X": "A", "Y": "B", "Z": "C"}]

def toLose(a):
    if a == "A":
        return "C"
    if a == "B":
        return "A"
    else:
        return "B"
def toWin(a):
    return winMap[a]
def toDraw(a):
    return a

def t2():
    inp = open("example", "r").readlines()
    score = 0
    for line in inp:
        opmove = line[0]
        res = line[2]
        if res == "X":
            target = toLose(opmove)
        elif res == "Y":
            target = toDraw(opmove)
            score += 3
        else:
            target = toWin(opmove)
            score += 6
        score += scoreMap[target]
    print(score)
t2()

def t1():
    inp = open("input", "r").readlines()
    for m in genMaps():
        score = 0
        for line in inp:
            cur = m[line[2]]
            score += scoreMap[cur] + calcWin(line[0], cur)
        print(score)


