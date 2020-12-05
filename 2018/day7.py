import networkx as nx
import re


def next_node_to_process(available):
    return sorted(available)[0]

# def process(node, diGraph, available):


class Task():
    def __init__(self, letter):
        self.time = ord(letter) - ord("A") + 60
        self.timeLeft = int(self.time)
        self.task = letter

    def isDone(self):
        return self.timeLeft < 0

    def tick(self):
        self.timeLeft -= 1
        return True

    def __str__(self):
        return self.task


def workersNotWorking(workerList):
    for i in workerList:
        if i["task"] != None:
            return False
    return True


if __name__ == "__main__":
    edges = []
    with open("day7.input") as inputFile:
        for line in inputFile:
            lineMatched = re.match(
                "Step (.) must be finished before step (.) can begin.",
                line
            )
            parent, child = lineMatched.groups()
            edges.append((parent, child))

    # Add the diGraph
    dg = nx.DiGraph()
    dg.add_edges_from(edges)

    # This will contain all currently available deps:
    available = set([node for node in dg if len(dg.in_edges(node)) < 1])

    output = ""
    #  PART1
    # while len(available) > 0:
    #     next_node = next_node_to_process(available)
    #     output += next_node
    #     available.remove(next_node)

    #     for node in list(dg.successors(next_node)):
    #         dg.remove_edge(next_node, node)
    #         if len(dg.in_edges(node)) < 1:
    #             available.add(node)
    workers = []
    workerAmount = 4
    for i in range(workerAmount):
        workers.append({"task": None})

    processed = 0
    while len(available) > 0 or not workersNotWorking(workers):
        for i in workers:
            if i["task"] == None and len(available) > 0:
                next_node = next_node_to_process(available)
                i["task"] = Task(next_node)
                available.remove(next_node)
            if i["task"] != None:
                i["task"].tick()
                if i["task"].isDone():
                    output += i["task"].task
                    for node in list(
                        dg.successors(i["task"].task)
                    ):
                        dg.remove_edge(i["task"].task, node)
                        if len(dg.in_edges(node)) < 1:
                            available.add(node)
                    i["task"] = None
                    if len(available) > 0:
                        next_node = next_node_to_process(available)
                        i["task"] = Task(next_node)
                        available.remove(next_node)
        print("{}\t\t{}\t\t{}\t\t{}".format(
            processed, workers[0]["task"], workers[1]["task"], output))
        processed += 1

    print(output)
