
inp = open("day13.input").readlines()
ts = int(inp[0])
busses = [int(x) for x in inp[1].strip().split(",") if x != "x"]
print(ts, busses)

minutes = 0
while not any(map(lambda n: (ts+minutes) % n == 0, busses)):
    minutes += 1
bus = list(filter(lambda n: (ts+minutes) % n == 0, busses))

print(ts+minutes, bus, minutes*bus[0])
schedule = [int(x) for x in inp[1].strip().replace("x", "-1").split(",")]

nb = []
for i in range(len(schedule)):
    if schedule[i] == -1:
        continue
    nb += [(i, schedule[i])]


n, a =  zip(*nb)
print(n, a)

stepSize = 1
waiting = True
ts = stepSize
#i = 1
broken = False
for i in range(len(a)):
    while (ts+n[i]) % a[i] != 0:
        ts += stepSize
    print(f"Found ts {ts} satisfying bus {i}, {a[i]}")
    stepSize *= a[i]

print(ts)
print("#"*80)
