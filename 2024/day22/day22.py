from collections import Counter
from multiprocessing import Pool
from pprint import pprint
prod = True
inp = """\
1
2
3
2024
""".rstrip()

with open("input") as f:
    if prod:
        inp = f.read()
        inp.rstrip()
inp = filter(lambda l: len(l) >= 1, inp.split("\n"))

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def rand(seed: int) -> int:
    a = prune(mix(seed, seed * 64))
    b = prune(mix(a // 32, a))
    c_ = b*2048
    c__ = mix(c_, b)
    return prune(c__)

seeds = list(map(int, inp))

#seeds = [123]
target = 2000
finals = []
prices = []
for num in seeds:
    c = [num % 10]
    #print(num, end=" ")
    s = num
    for i in range(target):
        s = rand(s)
        c.append(s % 10)
    finals += [s]
    prices.append(c)
changes = []
print((seeds))
for parr in prices:
    c = []
    for i in range(1, len(parr)):
        c.append(parr[i] - parr[i - 1])
    changes.append(c)
#print(changes)
possibilities = Counter()
for parr, carr in zip(prices, changes):
    highest = max(parr)
    for i in range(3, len(parr)):
        if parr[i] != highest:
            continue
        possibilities[(carr[i - 4], carr[i-3], carr[i-2], carr[i - 1])] += 1
#print(possibilities.most_common(10))
#print(len(possibilities))
#print(possibilities[(-2, 1, -1, 3)])
#print(prices)
#print(sum(finals))
#print(len(prices), len(prices[0]))

def runsim(seq, parr, carr):
    a, b, c, d = seq
    for i in range(len(carr) - 3):
        if carr[i] != a:
            continue
        if carr[i + 1] != b:
            continue
        if carr[i + 2] != c:
            continue
        if carr[i + 3] != d:
            continue
        return parr[i+4]
    return 0

high = 0
i = 0
nprocs = 24
pcarr = list(zip(prices, changes))
#def f(el):
    #return runsim(e[0], el[1], el[2])
seqs = [e for e, c in possibilities.most_common(len(possibilities))]
#for e, c in possibilities.most_common(len(possibilities)):
#    pass
def runseq(e):
    s = 0
    for parr, carr in zip(prices, changes):
        s += runsim(e, parr, carr)
    return s
p = Pool(nprocs)
outs = p.map(runseq, seqs)
p.close()
print(max(outs))
#i = 0
    #i += 1
    #if i == 10:
        #break
