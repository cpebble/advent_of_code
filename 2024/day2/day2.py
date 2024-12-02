
prod = True

inp = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""".split("\n")
with open('input') as f:
    if prod: 
        inp = f.readlines()


inp = list(map(lambda s: list(map(int, s.split(" "))), inp))

def issafe(report):
    increasing = report[0] < report[1]
    for i in range(1, len(report)):
        d_ =(report[i] - report[i-1]) 
        if increasing and d_ < 0: return False
        if not increasing and d_ > 0: return False
        d = abs(d_)
        if d > 3 or d == 0: return False
    return True

def issafewithout(report, i):
    return issafe(report[:i] + report[i+1:])
def iskindasafe(report):
    increasing = report[0] < report[1]
    for i in range(1, len(report)):
        d_ =(report[i] - report[i-1]) 
        if increasing and d_ < 0: return issafewithout(report, i)
        if not increasing and d_ > 0: return issafewithout(report, i)
        d = abs(d_)
        if d > 3 or d == 0: return issafewithout(report, i)
    return True

s = 0
for rep in inp:
    if issafe(rep):
        s += 1
        continue
    for i in range(len(rep)):
        if issafewithout(rep, i):
            s += 1
            break

part1 = sum(map(lambda x: int(x), list(map(issafe, inp))))
print(part1)
part2 = sum(map(lambda x: int(x), list(map(iskindasafe, inp))))
print(s)

