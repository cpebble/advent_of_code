

inp = """3   4
4   3
2   5
1   3
3   9
3   3""".split("\n")
with open('input') as f:
    inp = f.readlines()
inp = list(map(lambda s: list(map(int, s.strip().split("   "))), inp))
(left, right) = zip(*inp)
left = sorted(left)
right = sorted(right)
s = 0
# Part 1
for (l,r) in zip(left, right):
    s += abs(l-r)

from collections import Counter
counter = Counter()
for c in right:
    counter[c] += 1
s2 = 0
for l in left:
    s2 += l * counter[l]

print(s2)
