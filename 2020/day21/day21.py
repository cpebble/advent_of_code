
from collections import defaultdict
import sys
import numpy as np
import re

TEST = False
inp = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)\
"""

with open("day21.input") as f:
    realin = f.read()

inp: str = realin if not TEST else inp

lines = []
alg_d = defaultdict(list)
for line in inp.splitlines():
    match = re.match(r"([^\(]*) \(contains (.*)\)", line)
    ingredients, allergens = match.groups()
    ings = set(re.findall(r"\w+", ingredients))
    algs = set(re.findall(r"\w+", allergens))
    lines += [(ings, algs)]
    for a in algs:
        alg_d[a].append(ings)
    if TEST: print(f"I: {ings}, A: {algs}")

all_ings = set()
#all_algs = set()
for (li, la) in lines:
    all_ings  = all_ings.union(li)
    #all_algs.union(la)

alg_i = {alg: set.intersection(*alg_d[alg]) for alg in alg_d}
not_allergen = all_ings - set.union(*alg_i.values())
print(not_allergen)
count = 0
print("counting")
for (li, _) in lines:
    count += len(li.intersection(not_allergen))
print(count)
#print(all_ings)

unidentified = list(alg_i.keys())
identified = set()
idents = []
i = 0
print(alg_i)
while len(unidentified) > 0:
    i+= 1
    # Take tightest known alg
    cur = unidentified.pop(0)
    candidates = alg_i[cur] - identified
    if len(candidates) != 1:
        if TEST: print(f"Popped {cur} but isn't deduceable. Candidates: {candidates}")
        unidentified.append(cur)
        continue
    ingid = candidates.pop()
    identified.add(ingid)
    idents.append((cur, ingid ))
    if TEST: print(f"""Identified {cur} as {ingid}
Identified is now: {identified}
    """)

print(",".join(map(lambda i: i[1], sorted(idents, key=lambda i: i[0]))))
