from os import read
from pprint import pprint
import re
from collections import deque

prod = True
inp = """\
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
""".rstrip()
inp2 = """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""
inp3 = """\
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
"""

inp = inp3
with open("input") as f:
    if prod:
        inp = f.read()
        inp.rstrip()

init, rules_ = inp.split("\n\n")

state = {}
for (wire, val) in re.findall(r"(.\d\d): (\d)", init):
    state[wire] = int(val)

#pprint(state)
rules = []
for (a, op, b, dst) in re.findall(r"(...) ([ANDXOR]+) (...) -> (...)",
                                  (rules_)):
    rules.append((a, op, b, dst))
#pprint(rules)

def runop(op, a, b):
    if op == "OR":
        return a | b
    if op == "AND":
        return a & b
    if op == "XOR":
        return a ^ b

rqueue = deque(rules)
while len(rqueue) > 0:
    (a, op, b, dst) = rqueue.popleft()
    if not (a in state) or not (b in state):
        rqueue.append((a, op, b, dst))
        continue
    state[dst] = runop(op, state[a], state[b])
    

zarr = list(map(lambda x: str(state[x]), sorted(filter(lambda e: e[0] == "z", state.keys()), reverse=True)))
zval = (int("".join(zarr), 2))
print(zval)
xarr = map(lambda x: str(state[x]), sorted(filter(lambda e: e[0] == "x", state.keys()), reverse=True))
xval = (int("".join(xarr), 2))
yarr = map(lambda x: str(state[x]), sorted(filter(lambda e: e[0] == "y", state.keys()), reverse=True))
yval = (int("".join(yarr), 2))

zlen = int(sorted(filter(lambda e: e[0] == "z", state.keys()), reverse=True)[0][1:])
zreal = xval + yval
zrealarr = bin(zreal)[2:]
# In case of underflow
zrealarr = "x"*(zlen - len(zrealarr)) + zrealarr
# In case of overflow
zrealarr = zrealarr[-zlen:]
#print(zlen, len(zrealarr), zrealarr)
#print((list(zarr), list(zrealarr)))
#mistakes = []
#for (i, (z, zr)) in enumerate((zip((zarr), (zrealarr)))):
    #if z != zr:
        #mistakes += [zlen - i]
    ##print(z, zr)
#pprint(mistakes)


#zwires = list(sorted(filter(lambda e: e[0] == "z", state.keys()), reverse=True))
#print(zwires)
def follow(rules, target):
    if target[0] in ["x", "y"]:
        return [target]
    (a, _, b, _) = next(filter(lambda x: x[3] == target, rules))
    return [target] + follow(rules, a) + follow(rules, b)
##
#mistakes = []
#for z in zwires:
    #k = int(z[1:])
    #trail = follow(rules, z)
    #if any([x[1] == z[1] and x[2] == z[2] for x in trail if x[0] in ["x", "y"]]):
        #mistakes += [(z)]#, trail)]
    ##if not f"x{k:02}" in trail or not f"y{k:02}" in trail:
        ##mistakes += [(z, trail)]
    #
#print("mistakes")
#pprint((mistakes))

numbits = 6
if prod:
    numbits = 45
def cleanbits(bits):
    s = {}
    for x in range(bits):
        s[f"x{x:02}"] = 1
        s[f"y{x:02}"] = 1
    return s
def bitflipped(bits, i):
    s = cleanbits(bits)
    s[f"x{i:02}"] = 0
    s[f"y{i:02}"] = 0
    return s

def run(state, rules):
    rqueue = deque(rules)
    state = state.copy()
    while len(rqueue) > 0:
        (a, op, b, dst) = rqueue.popleft()
        if not (a in state) or not (b in state):
            rqueue.append((a, op, b, dst))
            continue
        state[dst] = runop(op, state[a], state[b])
    return state

def follow2(rules, target, level = 4):
    if level == 0:
        return "..."
    if target[0] in ["x", "y"]:
        return target
    (a, op, b, _) = next(filter(lambda x: x[3] == target, rules))
    return f"({follow2(rules, a, level - 1)} {op} {follow2(rules, b, level - 1)})"

for i in range(numbits):
    s = bitflipped(numbits, i)
    s = run(s, rules)
    if s[f"z{i:02}"] != 1:
        #pprint(s)
        print(f"MISMATCH {i}")
        print(follow2(rules, f"z{i:02}"))

# MAnual debuggin'
print(follow2(rules, "z27"))
print(follow2(rules, "z28"))
print(follow2(rules, "z29"))
print(follow2(rules, "z30"))
#print(follow2(rules, "z24"))
#print(follow2(rules, "z25"))


# z24 <-> tgr
# z12 <-> kwb 
# cph <-> jqn
# z16 <-> qkf

#cph,jqn,kwb,qkf,tgr,z12,z16,z24
