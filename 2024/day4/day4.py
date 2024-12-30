prod = True
inp = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".split("\n")
with open('input') as f:
    if prod: 
        inp = f.readlines()

count = 0
found = []
dirs = [
    (0,1),
    (0,-1),
    (1,0),
    (-1,0),
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1)
]
for r in range(len(inp)):
    for c in range(len(inp[r])):
        if inp[r][c] != "X":
            continue

        for (dy, dx) in dirs:
            try:
                for i in [r+dy*1,c+dx*1,r+dy*2,c+dx*2,r+dy*3,c+dx*3]:
                    if i < 0: raise Exception
                if inp[r+dy][c+dx] == "M" and inp[r+dy*2][c+dx*2] == "A" and inp[r+dy*3][c+dx*3] == "S":
                    count += 1
            except:
                pass
print(count)

# Part 2
c2 = 0
for r in range(1,len(inp)-1):
    for c in range(1,len(inp[r])-1):
        if inp[r][c] != "A":
            continue
        x1 = (inp[r-1][c-1] == "S" and inp[r+1][c+1] == "M") or\
             (inp[r-1][c-1] == "M" and inp[r+1][c+1] == "S")
        if not x1: continue
        x2 = (inp[r-1][c+1] == "S" and inp[r+1][c-1] == "M") or\
             (inp[r-1][c+1] == "M" and inp[r+1][c-1] == "S")
        if x2:
            c2 += 1
print(c2)
