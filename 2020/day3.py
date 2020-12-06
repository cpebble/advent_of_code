from math import ceil

inp = """\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#\
"""

#inp_arr = inp.split("\n")
inp_arr = [x.strip() for x in open("day3.input").readlines()]
pos = (0, 0)

slopes = [
(1,1),
(3,1),
(5,1),
(7,1),
(1,2)
]
res = 1
for dx, dy in slopes:

    trees = 0
    print("##")
    print(dx, dy)
    for i in range(ceil(len(inp_arr) / dy)):
        print(i, i*dx//dy)
        if inp_arr[i*dy][(i*dx) % len(inp_arr[0])] == "#":
            trees += 1
            print("#")
    res *= trees

print(res)

