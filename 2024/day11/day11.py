from functools import cache
prod = True
inp = "125 17"
with open('input') as f:
    if prod: 
        inp = f.read()
        inp.strip()

inp = inp
@cache
def countStones(val, blinks=0):
    if blinks == 0:
#        print(val)
        return 1
    if val == 0:
        return countStones(1, blinks-1)
    v = str(val)
    if len(v) % 2 == 0:
        v1 = int(v[:len(v) // 2])
        v2 = int(v[len(v) // 2:])
        return countStones(v1, blinks-1) + countStones(v2, blinks-1)
    return countStones(val*2024, blinks-1)

counts = 0
for i in inp.strip().split(" "):
    counts += countStones(int(i), 25)
print(counts)
counts = 0
for i in inp.strip().split(" "):
    counts += countStones(int(i), 75)
print(counts)

