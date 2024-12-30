from collections import defaultdict
from queue import Queue
from pprint import pprint
prod = True
inp = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

with open("input") as f:
    if prod:
        inp = f.read()
        inp.rstrip()
inp = inp.split("\n")

dirs = [
  (-1,0),(0,1),(1,0),(0,-1)
]
def run(inp, w, h, kb, sprint=False):
    dfield = defaultdict(lambda: False)

    i = 0
    for l in inp:
        x, y = l.split(",")
        x, y = int(x), int(y)
        
        dfield[(x, y)] = True
        i += 1
        if i >= kb:
            if sprint:
                print(x, y)
            break


    px,py = 0,0
    wq = Queue()
    wq.put((px, py, 0))
    visited = set()

    print("Running bfs")
    while wq.qsize() > 0:
        cx, cy, s = wq.get()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        # Goal
        if cx == w-1 and cy == h-1:
            return(cx, cy, s)
        # Check dirs
        for (dx, dy) in dirs:
            tmpx = cx + dx
            tmpy = cy + dy
            if (tmpx, tmpy) in visited:
                continue
            if tmpx >= 0 and tmpx < w and tmpy >= 0 and tmpy < h and not dfield[(tmpx, tmpy)]:
                wq.put((tmpx, tmpy, s + 1))
    return None
pprint("Ran")
#pprint(visited)
w, h, kb = 7,7, 12
if prod:
    w, h, kb = 71, 71, 1024

print(len(inp))
#low = kb
#high = len(inp)
low = 2953
high = 2954
while low < high - 1:
    mid = (low + high) // 2
    print(mid)
    res = run(inp.copy(), w, h, mid)
    # if can't find path
    if res == None:
        high = mid
    else:
        low = mid
    print(f"{res}, high is now {high}, low is now {low}")

print(inp[high+1])

print(run(inp, w, h, 2954, sprint=True))
#print(run(w, h, kb))
