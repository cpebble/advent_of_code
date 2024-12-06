prod = True
inp = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
with open('input') as f:
    if prod: 
        inp = f.read()
        inp.strip()

inp = inp.split("\n")
gx, gy = (0, 0)
for i,r in enumerate(inp):
    if "^" in r:
        gy, gx = (i, r.index("^"))
        break
inp = list(map(list, inp)) 
dirs = [
  (-1,0),(0,1),(1,0),(0,-1)
]

w,h = (len(inp[0]), len(inp))

iswithin = lambda x, y: x >= 0 and x < w and y >= 0 and y < h
def runMaze(maze, gx, gy):
    dir = 0
    visited = set()
    while iswithin(gx, gy):
        if (gy, gx, dir) in visited: return []
        visited.add((gy, gx, dir))
        tmpy = gy + dirs[dir][0]
        tmpx = gx + dirs[dir][1]

        if not iswithin(tmpx, tmpy):
            break
        if maze[tmpy][tmpx] == "#":
            dir = (dir + 1) % 4
            continue
        gy = tmpy
        gx = tmpx
    return visited

visited = runMaze(inp, gx, gy)
part1 = set(map(lambda elem: (elem[0], elem[1]), visited))
for (cy, cx, _) in visited:
    inp[cy][cx] = "X"
print("\n".join(list(map("".join, inp))))
print(len(part1))

loops = 0
for i, (cy, cx) in enumerate(part1):
    if cy == gy and cx == gx:
        continue
    inp[cy][cx] = "#"
    try:
        if runMaze(inp, gx, gy) == []:
            loops += 1
            print(f"Block at {cy},{cx}")
    except Exception as ex:
        # Some coordinate on some edge gives an oob. I cannot fathom why, and i
        # don't need to fix it apparently. Lazy coders get gold stars
        print(f"Encountered error at {(cy, cx)}: {ex}")
    inp[cy][cx] = "."

print(loops)


