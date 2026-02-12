
TEST = False
DEBUG = False
moves = 100
inp = """389125467"""

inp: str = "368195742" if not TEST else inp

class Cup():
    def __init__(self, id):
        self.id: int = id
        self.left: Cup | None = None
        self.right: Cup | None = None
    def insertLeft(self, left: Cup):
        """Insert a cup to the left of this one
        1. if curLeft is a cup, update its "right"
        2. set my left to new left
        3. set new left.left to my old left
        4. set new left.right to me
        """
        curLeft = self.left
        if curLeft != None:
            curLeft.right = left
        self.left = left
        left.left = curLeft
        left.right = self
    def insertRight(self, right: Cup):
        if self.right == None:
            self.right = right
            right.left = self
        else:
            self.right.insertLeft(right)
    def take(self):
        if self.right != None:
            self.right.left = self.left
        if self.left != None:
            self.left.right = self.right
        self.left = None
        self.right = None
        return self
    def ID(self):
        return self.id
    def __str__(self):
        return str(self.id)
    def __repr__(self):
        return f"<{self.left} - {self} - {self.right}>"


def printCupChain(start: Cup):
    seen = set()
    current = start
    out = []
    while current != None and not current in seen:
        seen.add(current)
        out.append(str(current.id))
        current = current.right
    return ", ".join(out)

cups = list()
onecup = None
prev = None
for n in inp:
    i = int(n)
    c = Cup(i)
    if i == 1: onecup = c
    cups.append(c)
    if prev != None:
        prev.insertRight(c)
    prev = c
cups[0].left = prev
cups[-1].right = cups[0]
current = cups[0]

# Sort cups list
if DEBUG: print(cups)
# Setup is done

if DEBUG: print(printCupChain(current))
def move(c, highest=9):
    if DEBUG: print("Current: ", c)
    picked_up = [c.right.take(), c.right.take(), c.right.take()]
    picked_up_ids = list(map(Cup.ID, picked_up))
    if DEBUG: print("Picked up: ", picked_up_ids)
    
    # Find destination id
    dest_id = c.id - 1
    while True:
        if dest_id < 1:
            dest_id = highest
            continue
        if dest_id in picked_up_ids:
            dest_id -= 1
            continue
        break
    if DEBUG: print("Destination: ",dest_id)
    next = c.right
    while next.id != dest_id:
        assert next != c, f"Looped, but didn't find {dest_id}"
        next = next.right
    picked_up.reverse()
    for cup in picked_up:
        next.insertRight(cup)
    

## The crab picks up the three cups that are immediately clockwise of the
# current cup. They are removed from the circle; cup spacing is adjusted as
# necessary to maintain the circle.

## The crab selects a destination cup: the cup with a label equal to the current
# cup's label minus one. If this would select one of the cups that was just
# picked up, the crab will keep subtracting one until it finds a cup that
# wasn't just picked up. If at any point in this process the value goes below
# the lowest value on any cup's label, it wraps around to the highest value on
# any cup's label instead.

## The crab places the cups it just picked up so that they are immediately
# clockwise of the destination cup. They keep the same order as when they were
# picked up.

## The crab selects a new current cup: the cup which is immediately clockwise of
# the current cup.

# Assemble answer
def part1(start, astart):
    i = 0
    current = start
    while i < moves:
        if DEBUG: print(f"--- Move {i} ---")
        i += 1
        if DEBUG: print(printCupChain(current))
        move(current)
        current = current.right
    seen = set()
    out = ""
    c = astart
    while not c in seen:
        seen.add(c)
        out += str(c)
        c = c.right
    return out[1:]
#print(part1(cups[0], onecup))

def part2(inp):
    c0 = Cup(int(inp[0]))
    c1 = None
    allcups = [None]*1000000
    allcups[c0.id-1] = c0
    prev = c0
    for i in inp[1:]:
        c = Cup(int(i))
        if c.id == 1: c1 = c
        prev.right = c
        c.left = prev
        allcups[c.id - 1] = c
        prev = c
    if DEBUG: breakpoint()
    for i in range(10, 1000001):
        c = Cup(i)
        prev.right = c
        c.left = prev
        allcups[c.id - 1] = c
        prev = c
    # Close the chain
    prev.right = c0
    c0.left = prev
    pass
    c = c0
    for i in range(10_000_000):
        #if i % 100 == 0:
            #print(i)
        # move(current, highest=1000000)
        # Execute move
        picked_up = [c.right, c.right.right, c.right.right.right]
        picked_up_ids = [c_.id for c_ in picked_up]
        c.right = c.right.right.right.right
        c.right.left = c
        # Find destination id
        dest_id = c.id - 1
        while True:
            if dest_id < 1:
                dest_id = 1000000
                continue
            if dest_id in picked_up_ids:
                dest_id -= 1
                continue
            break
        dest = allcups[dest_id - 1]
        # Take dest + 1
        if dest == None:
            breakpoint()
        dest_p1 = dest.right
        # Fix left side link
        dest.right = picked_up[0]
        picked_up[0].left = dest
        # Fix right side link
        dest_p1.left = picked_up[2]
        picked_up[2].right = dest_p1
        c = c.right
    #breakpoint()
    print(c1, c1.right, c1.right.right)
    print(c1.right.id * c1.right.right.id)

import cProfile
cProfile.run('part2(inp)', 'profile2')

