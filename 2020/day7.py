import re

testinput = """\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.\
"""
accepted_bags = ["shiny gold"]
for line in testinput.split("\n"):
    a = line.split(" contain ")[0]
    b = line.split(" contain ")[1]
    #for t in b.split(","):
    for acc in accepted_bags:
        if re.search("shiny gold bag", t):
            print(a)

