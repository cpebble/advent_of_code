
chars = [".", "#", "L"]

inp = open("day11.input").readlines()

_grid = []

def pgrid(grid):
    print("#"*80)
    for r in range(len(grid)):
        for c in range(len(grid)):
            print(grid[r][c], end="")
        print("")

for line in inp:
    l = line.strip()
    larr = [c for c in l]
    _grid.append(larr)

print(_grid)

def neighbors(grid, x, y, part2=False):
    _n = 0
    state = grid[y][x]
    for (dx, dy) in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        try:
            nx, ny = (x + dx, y + dy)
            while part2 and (nx >= 0 or ny >= 0) and (grid[ny][nx] == "."):
                nx, ny = (nx + dx, ny + dy)
            if nx < 0 or ny < 0:
                continue
            if grid[ny][nx] == "#":
                _n += 1
        except:
            pass
    return _n

def deepcopy(a):
    x = []
    for r in a:
        x.append([e for e in r])

    return x

def step(grid):
    changed = False
    ngrid = deepcopy(grid)
    occupied = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            state = grid[y][x]
            n = neighbors(grid, x, y)
            #print(x, y, "found",n, "is", state, state == "L")
            if state == "L" and n == 0:
                ngrid[y][x] = "#"
                changed = True
            elif state == "#" and n >= 4:
                ngrid[y][x] = "L"
                changed = True
    if not changed:
        return ngrid
    else:
        return step(ngrid)
_grid1 = step(_grid)

#pgrid(_grid)
print(sum([1 for r in _grid1 for c in r if c == "#"]))


def step2(grid):
    changed = False
    ngrid = deepcopy(grid)
    occupied = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            state = grid[y][x]
            n = neighbors(grid, x, y, True)
            #print(x, y, "found",n, "is", state, state == "L")
            if state == "L" and n == 0:
                ngrid[y][x] = "#"
                changed = True
            elif state == "#" and n >= 5:
                ngrid[y][x] = "L"
                changed = True
    if not changed:
        return ngrid
    else:
        return step2(ngrid)
_grid2 = step2(_grid)
print("ran step 2")
print(sum([1 for r in _grid2 for c in r if c == "#"]))





print("Testing grid")
tgrid = [ r for r in """\
#######
#######
#######
#######
#######
#######
#######\
""".split("\n")]
pgrid(tgrid)
print(neighbors(tgrid, 3, 3, True))









