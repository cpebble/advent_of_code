prod = False

inp = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
if prod:
    with open("input") as f:
        inp = f.read().strip()

inp = inp.split("\n")

def evaleq(target, acc, eqn):
    if eqn == []:
        return int(target == acc)
    c = eqn[0]
    v1 = evaleq(target, acc*c, eqn[1:])
    if v1 > 0:
        return v1
    v1 = evaleq(target, acc+c, eqn[1:])
    if v1 > 0:
        return v1
    v1 = evaleq(target, int(str(acc) + str(c)), eqn[1:])
    if v1 > 0:
        return v1
    return 0

counts = 0
for line in inp:
    target, eqn = line.split(":")
    target = int(target)
    eqn = list(map(int, eqn.strip().split(" ")))
    solutions = evaleq(target, 0, eqn)
    if solutions > 0:
        counts += target
print(counts)

