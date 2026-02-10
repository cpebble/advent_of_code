import numpy as np

TEST = True
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

    def __str__(self) -> str:
        out = f"Tile: {self.id}\n"
        for r in range(self.h):
            for c in range(self.w):
                out += self.get(r, c)
            out += "\n"
        return out

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
    def flipX(self):
        self.fX = not self.fX

    def flipY(self):
        self.fY = not self.fY

 
tiles = list([Tile(t) for t in inp.split("\n\n")])
print(tiles[0])
tiles[0].flipX()
print(tiles[0])
#print(tiles[0])
#tiles[0].rotate()
#print(tiles[0])
#tiles[0].rotate()


# Try to determine final construction
width = np.sqrt(len(tiles)).astype(int)
assert width*width == len(tiles)
print(width)
