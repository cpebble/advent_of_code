

inp = [int(x.strip()) for x in open("day10.input").readlines()]

in_s = sorted(inp)
ones = 0
threes = 0
cur = 0
for i in range(len(in_s)):
    new = in_s[i]
    if new > cur+3:
       print(f"cannot make the jump from {cur} to {in_s[i]}")
       break
    if new == cur+3:
       threes += 1
    elif new == cur+1:
        ones += 1
    cur = new
print("P1", ones * (threes+1))

# Part 2
solutions = {}
deb = []
in_ = [0] + in_s
def combinations(i):
    global deb
    global solutions
    # Base case
    if i == len(in_) - 1:
        return 1
    if i in solutions:
        return solutions[i]

    # Recursive case
    s = 0
    for j in range(i+1, len(in_)):
        if in_[j] <= in_[i] + 3:
            s += combinations(j)
    solutions[i] = s
    return s
print(combinations(0))

