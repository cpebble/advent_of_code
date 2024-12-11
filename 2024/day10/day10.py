from queue import Queue
prod = True

inp = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""".split("\n")
with open('input') as f:
    if prod: 
        inp = f.readlines()

inp = list(map(lambda l: list(map(int, l.strip())), inp))

trailheads = []
for r in range(len(inp)):
    for c in range(len(inp[r])):
        if inp[r][c] == 0:
            trailheads.append((r, c))

dirs = [
  (-1,0),(0,1),(1,0),(0,-1)
]
def trailheadscore(maze, r, c):
    h, w = len(maze), len(maze[0])
    toVisit = Queue()
    count = set()
    toVisit.put((r,c))
    while toVisit.qsize() > 0:
        cr, cc = toVisit.get()
        v = maze[cr][cc]
        if v == 9:
            count.add((cr, cc))
            continue
        for (dr, dc) in dirs:
            nr = cr + dr
            nc = cc + dc
            if nr >= 0 and nr < h and nc >= 0 and nc < w and maze[nr][nc] == v + 1:
                toVisit.put((nr, nc))
    return len(count)
def trailheadrating(maze, r, c):
    h, w = len(maze), len(maze[0])
    toVisit = Queue()
    count = 0
    toVisit.put((r,c))
    while toVisit.qsize() > 0:
        cr, cc = toVisit.get()
        v = maze[cr][cc]
        if v == 9:
            count+=1
            continue
        for (dr, dc) in dirs:
            nr = cr + dr
            nc = cc + dc
            if nr >= 0 and nr < h and nc >= 0 and nc < w and maze[nr][nc] == v + 1:
                toVisit.put((nr, nc))
    return count
scores = [trailheadscore(inp, r, c) for (r, c) in trailheads] 

print(scores)
print(sum(scores))
ratings = [trailheadrating(inp, r, c) for (r, c) in trailheads] 

print(ratings)
print(sum(ratings))
