import re
from json import dumps
f = "day7.input"
bags = set()
bags = {}

class Bag():
    def __init__(self, name):
        self.name = name
        self.parents = set()
        self.children = set()
    def __str__(self):
        return self.name

def createBag(color):
    global bags
    bags[color] = {
            "children": {},
            "parents": []
            }
    return

def getAllParents(color):
    parents = set()
    bag = bags[color]
    parents = set(bag["parents"])
    for p in bag["parents"]:
        parents = parents | getAllParents(p)
    return parents

def getBagValue(color):
    count = 1
    bag = bags[color]
    for c in bag["children"]:
        print(f"bag {color} has child {c} with count {bag['children'][c]}")
        count += getBagValue(c) * bag["children"][c]
    return count

for line in open(f).readlines():
    s = line.split(" contain ")
    bagstring = re.findall(r"(\d )?(\w* \w*) bags?", line)
    first = True
    bag = None
    for count, color in bagstring:
        # Parse no children
        if color == "no other":
            continue
        # Ensure found bag exists
        if color not in bags:
            createBag(color)
        # Parse first bag
        if first:
            bag = color
            first = False
            continue

        # Add to set
        bags[color]["parents"].append(bag)
        bags[bag]["children"][color] = int(count.strip())
#print(dumps(bags))
print(len(getAllParents("shiny gold")))
print(getBagValue("shiny gold") - 1)
