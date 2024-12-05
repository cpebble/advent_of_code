prod = True
inp = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
with open('input') as f:
    if prod: 
        inp = f.read()


(rules, updates) = inp.split("\n\n")

from collections import defaultdict
rmap = defaultdict(list)
lmap = defaultdict(list)
for rule in rules.split("\n"):
    l,r = rule.split("|")
    rmap[int(l)].append(int(r))
    lmap[int(r)].append(int(l))

def iscorrect(update):
    canthave = set()
    for num in update:
        if num in canthave:
            return False
        canthave.update(lmap[num])
    # If we made it here, no exceptions
    return True
    

correct = []
incorrect = []
for update in updates.strip().split("\n"):
    up = list(map(int,update.split(",")))
    if iscorrect(up):
        correct.append(up)
    else:
        incorrect.append(up)
(mids := [c[len(c)//2] for c in correct])
print(sum(mids))

def fixupdate(update):
    if len(update) == 1:
        return update
    startnum = -1
    for x in update:
        it = True
        for y in update:
            if y in lmap[x]:
                it = False
                break
        if it:
            startnum = x
    return [startnum] + fixupdate(list(filter(lambda n: n != startnum, update)))

#fixupdate([75,97,47,61,53])

fixed = []
for update in incorrect:
    tmp = fixupdate(update)
    assert(iscorrect(tmp))
    fixed.append(fixupdate(update))
       
print(fixed)
(mids2 := [c[len(c)//2] for c in fixed])
print(sum(mids2))
