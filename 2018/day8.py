
inputs = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]


def readHeader(A, i):
    return (A[i], A[i+1])


nodes = []


def process(A, j):
    """ Takes the "head" node, returns a dict containing: {metadata: [], children: [], length: int} """
    childrenCount, metadataCount = readHeader(A, j)
    curOff = j+2
    children = []
    for i in range(childrenCount):
        child = process(A, curOff)
        children.append(child)
        curOff += child["length"]
    metadata = []
    for i in range(metadataCount):
        metadata += [A[curOff]]
        curOff += 1
    me = {"children": children, "metadata": metadata, "length": curOff-j}
    nodes.append(me)
    return me


def node_value(node):
    if len(node["children"]) < 1:
        return sum(node["metadata"])
    value = 0
    for data in node["metadata"]:
        if 0 < data <= len(node["children"]):
            value += node_value(node["children"][data-1])
    return value


if __name__ == "__main__":
    with open("day8.input") as inputfile:
        input_array = list(map(int, inputfile.readline().split()))
    tree = process(input_array, 0)
    mSum = 0
    for n in nodes:
        mSum += sum(n["metadata"])
    print(mSum)
    print(node_value(tree))
