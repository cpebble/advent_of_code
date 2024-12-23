from collections import defaultdict
from pprint import pprint
import re

prod = True
inp = '''\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn'''

if prod:
    with open("input") as f:
        inp = f.read()

edges = set()
nodes = set()
for (a, b) in re.findall(r'(..)-(..)', inp):
    nodes.add(a)
    nodes.add(b)
    edges.add((a, b))
    edges.add((b, a))

#print(nodes)

#triangles = set([
#        (a, b, c) 
#        for a in nodes
#        if a[0] == 't'
#        for b in nodes - set((a,))
#        if (a, b) in edges
#        for c in nodes - set((a, b))
#        if (b, c) in edges
#        if (c, a) in edges])
triangles = set()
snodes = list(sorted(nodes))
for i in range(len(snodes)):
    a = snodes[i]
    for j in range(i + 1, len(snodes)):
        b = snodes[j]
        if not (a, b) in edges:
            continue
        for k in range(j + 1, len(snodes)):
            c = snodes[k]
            if not (a, c) in edges:
                continue
            if not (b, c) in edges:
                continue
            triangles.add((a, b, c))
            
#print(triangles)
print(len(triangles))

ttriangles = set(filter(lambda el: el[0][0] == 't' or el[1][0] == 't' or el[2][0] == 't', triangles))

#print(ttriangles)
print(len(ttriangles))
nmap = defaultdict(list)
for (a, b) in edges:
    nmap[a].append(b)

print(nmap['ta'])

visited = set()
biggest = []

sets = [set([a]) for a in nodes]
for s in sets:
    for x in nodes:
        if all([(x, y) in edges for y in s]): s.add(x)
print(",".join(sorted(sorted(sets, key=len, reverse=True)[0])))

