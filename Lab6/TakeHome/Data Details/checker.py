# Read file network.txt and check if there exists any duplicate edges
# If there exists any duplicate edges, print the edge and the number of times it is repeated
# If there are no duplicate edges, print "No duplicate edges found"

import sys

data = open("network.txt", "r").readlines()
edges = set()
for line in data:
    nodes = line.strip().split(" ")
    if nodes[0] in edges:
        print(f"Duplicate edge: {nodes[0]}")
    else:
        edges.add(nodes[0])