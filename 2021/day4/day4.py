
c = []
with open("input", "r") as ex:
    c = ex.readlines()
seq = list(map(lambda n: int(n), c[0].split(",")))

def parseBoards(l):
    r = []
    for i in range(len(l) // 5):
        r_ = []
        offset = i*6
        for l_ in l[offset+1:offset+6]:
            r_ += [[int(x) for x in l_.replace("  ", " ").strip().split(" ")]]
        r += [r_]

    return [r_ for r_ in r if r_ != []]

boards = parseBoards(c[1:])

def updateLine(line, number):
    return [e if e != number else 0 for e in line]

def updateBoard(board, number):
    return [updateLine(l, number) for l in board]

def updateBoards(boards, number):
    return [updateBoard(board, number) for board in boards]

def findWinningBoards(boards):
    # Find Horizontal
    for b in boards:
        for l in b:
            if all(map(lambda e: e == 0, l)):
                return b
    # Find vertical
    for b in boards:
        for i in range(5):
            tmp = True
            for l in b:
                tmp = tmp and l[i] == 0
            if tmp:
                return b
    return None

#print(findWinningBoards(updateBoards(test,999)))

def runSeq(seq, boards):
    b = boards
    for i in range(len(seq)):
        b = updateBoards(b, seq[i])
        if findWinningBoards(b) != None:
            return (i, seq[:i], findWinningBoards(b))
    return (None,None,None)

def runSeq2(seq, boards):
    b = boards
    bi = 0
    wb = []
    for i in range(len(seq)):
        b = updateBoards(b, seq[i])
        while findWinningBoards(b) != None:
            print(f"Found winning board at: {i} {seq[i]}")
            b_ = findWinningBoards(b)
            a = len(b)
            b_str = str(b_)
            b = list(filter(lambda x: str(x) != b_str, b))
            bx = len(b)
            print(f"a: {a}, b: {bx}")
            wb += [(i, b_)]
    print(wb[-1])
    return (wb[-1])

(i, seq2, b) = runSeq(seq, boards)
#print("$$$$$$$$", i, seq2, b)
res = (sum([sum(l) for l in b]))
print(res*seq[i])

(i, b) = runSeq2(seq, boards)
res = (sum([sum(l) for l in b]))

print(res*seq[i])
