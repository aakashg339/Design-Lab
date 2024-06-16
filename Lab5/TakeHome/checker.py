import networkx as nx

# Read file network.txt with values format u,v where u and v are integers.
G = nx.read_edgelist("network.txt", delimiter=",", nodetype=int)

# Sort the nodes by degree in descending order and print the top 10 nodes with highest degree.
degree = G.degree()
sorted_degree = sorted(degree, key=lambda x: x[1], reverse=True)
print("Top 10 nodes with highest degree:")
for i in range(10):
    print(sorted_degree[i])

# Get nodes that are neighbors of the top 10 nodes.
neighbors = {}
for i in range(10):
    node_id = sorted_degree[i][0]
    neighbors[node_id] = list(G.neighbors(node_id))

print("Neighbors of top 10 nodes:")
print(neighbors)

# Get the union of the neighbors of the top 10 nodes and print the size of the union
union = set()
for i in range(10):
    union = union.union(neighbors[sorted_degree[i][0]])

print("Size of union of neighbors of top 10 nodes: {}".format(len(union)))
