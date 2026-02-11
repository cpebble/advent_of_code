import sys
import numpy as np

TEST = False
inp = """\
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...\
"""
with open("day20.input") as f:
    realin = f.read()

inp = realin if not TEST else inp
class Tile():
    def __init__(self, text: str):
        id_s, *grid_s = text.splitlines()
        self.id = int(id_s[5:9])
        grid = [list(l.strip()) for l in grid_s]
        self.grid = np.array(grid)
        self.inner = self.grid[1:-1,1:-1]
        self.w = len(self.grid[0])
        self.h = len(self.grid)
        self.rotation = 0
        self.fX = False
        self.fY = False

    def get(self, r, c) -> str:
        g = self.grid
        if self.fX:
            g = np.fliplr(g)
        if self.fY:
            g = np.flipud(g)
        return np.rot90(g, self.rotation)[r][c]

    def iget(self, r, c) -> str:
        g = self.inner
        if self.fX:
            g = np.fliplr(g)
        if self.fY:
            g = np.flipud(g)
        return np.rot90(g, self.rotation)[r][c]

    def __str__(self) -> str:
        out = f"Tile: {self.id}\n"
        for r in range(self.h):
            for c in range(self.w):
                out += self.get(r, c)
            out += "\n"
        return out
    def getInner(self):
        g = self.grid
        if self.fX:
            g = np.fliplr(g)
        if self.fY:
            g = np.flipud(g)
        return np.rot90(g, self.rotation)[1:-1,1:-1]
    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
    def flipX(self):
        self.fX = not self.fX

    def flipY(self):
        self.fY = not self.fY

    def border(self, nesw: int = 0):
        return np.rot90(self.grid, nesw)[0,:]

    def toprow(self):
        g = self.grid
        if self.fX:
            g = np.fliplr(g)
        if self.fY:
            g = np.flipud(g)
        return np.rot90(g, self.rotation)[0,:]
    def leftcol(self):
        g = self.grid
        if self.fX:
            g = np.fliplr(g)
        if self.fY:
            g = np.flipud(g)
        return np.rot90(g, self.rotation)[:,0]
    def rightcol(self):
        g = self.grid
        if self.fX:
            g = np.fliplr(g)
        if self.fY:
            g = np.flipud(g)
        return np.rot90(g, self.rotation)[:,-1]
    def bottomrow(self):
        g = self.grid
        if self.fX:
            g = np.fliplr(g)
        if self.fY:
            g = np.flipud(g)
        return np.rot90(g, self.rotation)[-1,:]

 
tiles = list([Tile(t) for t in inp.split("\n\n")])
#print(tiles[0])
#print(tiles[0].border(0))
#print(tiles[0].border(1))
#print(tiles[0].border(2))
#print(tiles[0].border(3))


# Try to determine final construction
width = np.sqrt(len(tiles)).astype(int)
assert width*width == len(tiles)

# available = set(tiles)
#matches = {}
#for t in tiles:
    ## Try to map borders
    #ms = 0
    #matches[t.id] = {}
    #for d in range(4):
        #border = t.border(d)
        #matches[t.id][d] = None
        #for t_ in available:
            ## Not same
            #if t_ == t:
                #continue
            ## Match sub=border
            #for d_ in range(4):
                #if np.all(t_.border(d_) == border) or np.all(np.flip(t_.border(d_)) == border):
                    #assert matches[t.id][d] == None
                    #matches[t.id][d] = t_.id
#
#corners = [
        #tid
        #for (tid, tms) in matches.items()
        #if len(list(filter(bool, tms.values()))) == 2
    #]
#matchset = {
        #tid: set(tms.values()) - set([None])
        #for (tid, tms) in matches.items()
    #}
#print(np.prod(corners))


tilemap = {t.id: t for t in tiles}

assembled = [[None for _ in range(width)] for _ in range(width)]

if not TEST:
    assembled[0][0] = 2879
else:
    assembled[0][0] = 2971

available = set([t.id for t in tiles])
collected = set()
collected.add(assembled[0][0])
for r in range(width):
    for c in range(width - 1):
        # Take current id
        cur_id = assembled[r][c]
        if c == 0 and r != width - 1: # Also need to populate below
            sbord = tilemap[cur_id].bottomrow()
            found = False
            for p_id in available - collected:
                if found: break
                p_tile = tilemap[p_id]
                for rotation in range(4):
                    nbord = p_tile.toprow()
                    if np.all(np.flip(nbord) == sbord):
                        if rotation % 2 == 0:
                            p_tile.flipX()
                        else:
                            p_tile.flipY()
                        nbord = p_tile.toprow()
                    if np.all(nbord == sbord):
                        collected.add(p_id)
                        assembled[r+1][c] = p_id
                        found == True
                        break
                    p_tile.rotate()
        rbord = tilemap[cur_id].rightcol()
        found = False
        for p_id in available - collected:
            if found: break
            p_tile = tilemap[p_id]
            for rotation in range(4):
                lbord = p_tile.leftcol()
                if np.all(np.flip(lbord) == rbord):
                    if rotation % 2 == 0:
                        p_tile.flipY()
                    else:
                        p_tile.flipX()
                    lbord = p_tile.leftcol()
                if np.all(lbord == rbord):
                    collected.add(p_id)
                    assembled[r][c+1] = p_id
                    found == True
                    break
                p_tile.rotate()

                        
                        
print(assembled)

ass_inner = [
    [
       tilemap[c_id].getInner() for c_id in row
    ] for row in assembled
]
rows = [
    np.concatenate(row, axis=1)
    for row in ass_inner
]
ass_np = np.concatenate(rows, axis=0)
print(ass_np.shape)
print(rows[0].shape)
ass_np = np.flipud(ass_np)
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
monster = [
        (1,1), (4, 1), (5,0), (6,0), (7, 1), (10, 1), (11, 0), (12, 0), (13, 1),
        (16, 1), (17, 0), (18, -1), (18, 0), (19, 0)
    ]

monsters = 0
for xflip in range(2):
    ass_np = np.fliplr(ass_np)
    if monsters != 0: break
    print("Flip X")
    for yflip in range(2):
        ass_np = np.flipud(ass_np)
        if monsters != 0: break
        print("Flip Y")
        for rotation in range(4):
            if monsters != 0: break
            print("Rotate")
            ass_np = np.rot90(ass_np, 1)
            for r in range(1, width*(tiles[0].w - 2) - 1):
                for c in range(1, width*(tiles[0].w - 2) - 18): 
                    if ass_np[r][c] == "#":
                        isMonster = True
                        for (dx, dy) in monster:
                            if ass_np[r+dy][c+dx] != "#":
                                isMonster = False
                                break
                        if isMonster:
                            monsters += 1
                            print("Found a monster")

print(np.sum(ass_np == "#") - monsters*15)
