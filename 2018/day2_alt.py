from collections import Counter

pairs, triples = (0, 0)
with open("advent_of_code/day2.input") as inputStrings:
    for inputs in inputStrings.readlines():
        letters = Counter(inputs)
        if letters.most_common()[0][1] == 2:
            pairs += 1
        if letters.most_common()[0][1] == 3:
            if letters.most_common()[1][1] == 2:
                pairs += 1
            triples += 1

print(pairs, triples, pairs*triples)
