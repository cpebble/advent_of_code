# Time to **: 15:37
from collections import Counter

ex = """\
abc

a
b
c

ab
ac

a
a
a
a

b\
"""
yx = open("day6.input").read().rstrip()

res = 0
groups = []
for group in yx.split("\n\n"):
    groupd = Counter()
    print("group is\n" + group)
    count = group.count("\n") + 1
    print("Count is " + str(count))
    amount = 0
    for x in group.replace("\n", ""):
        groupd[x] += 1

    res += sum([1 for x in groupd if groupd[x] == count])
print(res)



