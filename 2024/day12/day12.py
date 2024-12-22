from functools import cache
from queue import Queue
prod = True
inp = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
inp2 = """\
AAAA
BBCD
BBCC
EEEC"""
#inp = inp2
with open('input') as f:
    if prod: 
        inp = f.read()
        inp.strip()

inp = [list(l) for l in inp.strip().split('\n')]

visited = set()
h,w = len(inp), len(inp[0])
dirs = [
  (0,1),(1,0),(0,-1),(-1,0)
]

def explore(maze, r, c):
    rs = set()
    toVisit = Queue()
    toVisit.put((r, c))
    target = maze[r][c]
    pms = set()
    while toVisit.qsize() > 0:
        r, c = toVisit.get()
        if (r, c) in rs:
            continue
        rs.add((r, c))
        for dir in dirs:
            dr, dc = dir
            nr = r + dr
            nc = c + dc
            if nr >= 0 and nr < h and nc >= 0 and nc < w:
                if maze[nr][nc] == target:
                    #print(f"{nr, nc} is target {target}")
                    toVisit.put((nr, nc))
                    continue
            #print(f"{r, c} dir {dr, dc} is perimeter")
            pms.add((r, c, dir))
    return (rs, pms)


#def explore3(maze, r, c):
    #cr = r
    #cc = c
    #dir = 0
    #target = maze[r][c]
    #i = 0
    #while True and i < 100:
        #i+= 1
        #dr, dc = dirs[dir]
        #lr, lc = dirs[dir - 1]
        #def targetorwall(r, c):
            #if r < 0 or r >= h:
                #return True
            #if c < 0 or c >= w:
                #return True
            #return maze[r][c] == target
            #
        #while targetorwall(

def explore2(maze, r, c):
    rs = set()
    targetc = maze[r][c]
    pms = 0
    # Current pos
    cr = r
    cc = c
    dir = 0
    left = lambda: dirs[(dir - 1) % 4]
    first = True
    def target(r,c, err=True):
        try:
            return maze[r][c] == targetc
        except IndexError:
            return err
    i = 0
    import pdb
    pdb.set_trace()
    while True and i < 100:
        i+= 1
        if not first and cr == r and cc == c and dir == 0:
            break
        print(cr, cc)
        # We always want Not-target on our left side
        r_,c_ = left()
        if not target(cr + r_, cc + c_):
            # Great, continue to move
            # Edge case so we don't walk oob
            dr, dc = dirs[dir]
            nr = cr + dr
            nc = cc + dc
            if nr >= 0 and nr < h and nc >= 0 and nc < w and maze[nr][nc] == targetc:
                first = False
                cr = nr
                cc = nc
                # Check if we can turn left
                if target(cr + r_, cc + c_, False):
                    dir = (dir - 1) % 4
                    cr = cr + r_
                    cc = cc + c_
                    pms += 1
                continue
        # We want to turn
        pms += 1
        dir = (dir + 1) % 4
    return pms 
        


part1 = 0
part2 = 0
for r in range(h):
    for c in range(w):
        if (r,c) in visited:
            continue
        regionset, perimeter = explore(inp, r, c)
        #print(inp[r][c], regionset, len(regionset), perimeter)
        part1 += len(regionset)*len(perimeter)
        visited = visited.union(regionset)
        sides = 0
        while len(perimeter) > 0:
            pr, pc, pd = perimeter.pop()
            sides += 1
            i = 1
            while True:
                nr, nc = pr + (pd[1]*i), pc + (pd[0]*i)
                if (nr, nc, pd) in perimeter:
                    perimeter.remove((nr, nc, pd))
                    i += 1
                else:
                    break
            i = -1
            while True:
                nr, nc = pr + (pd[1]*i), pc + (pd[0]*i)
                if (nr, nc, pd) in perimeter:
                    perimeter.remove((nr, nc, pd))
                    i -= 1
                else:
                    break
            
        part2 += len(regionset)*sides

print(part1)
print(part2)

