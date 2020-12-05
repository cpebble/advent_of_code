import re


pattern = r".+(.).+\1"

pairs, triples = (0, 0)
pairPattern = re.compile(pattern)
triplePattern = re.compile(r".*(.).*\1.*\1")
with open("advent_of_code/day2.input") as inputStrings:
    for inputs in inputStrings.readlines():
        pmatches = re.match(pairPattern, inputs)
        tmatches = re.match(triplePattern, inputs)
        if pmatches and not tmatches:
            pairs += 1
            continue
        if tmatches and not pmatches:
            triples += 1
            continue
        pgroups = pmatches.groups()
        tgroups = tmatches.groups()
        if len(tgroups) == 1 and pgroups:
            if pmatches.group(1) != tmatches.group(1):
                triples += 1
                pairs += 1
            else:
                triples += 1

print(pairs, triples, pairs*triples)
