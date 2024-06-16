import sys

# Used to get the nodes which are having an edge to any one of the top 10 nodes with maximum frequency
class Reducer:
    def __init__(self):
        self.adjacencyList = {}

        for i in range(0, 300):
            self.adjacencyList[i] = []
    
    # Creating undirected graph as chatting happens in both directions
    def createAdjacencyList(self, currentKey, destinationNode):
        currentKey = int(currentKey)
        destinationNode = destinationNode.split(",")
        destinationNode = list(map(int, destinationNode))

        for node in destinationNode:
            if node not in self.adjacencyList[currentKey]:
                self.adjacencyList[currentKey].append(node)
            if currentKey not in self.adjacencyList[node]:
                self.adjacencyList[node].append(currentKey)

    def printArticulationPoints(self, articulationPoints):
        for node in articulationPoints:
            if articulationPoints[node] > 0:
                print(node)
    
    def initializeGraphAndVariables(self, visited, parent, low, disc, articulationPoints):
        for node in self.adjacencyList:
            visited[node] = False
            parent[node] = None
            low[node] = float("inf")
            disc[node] = float("inf")
            articulationPoints[node] = 0

    # Adjacency List is a directed graph
    def findArticulationPoints(self):
        visited = {}
        parent = {}
        lowValue = {}
        discoveryTime = {}
        articulationPoints = {}
        time = 0

        self.initializeGraphAndVariables(visited, parent, lowValue, discoveryTime, articulationPoints)

        for node in self.adjacencyList:
            if visited[node] == False:
                self.articulationPointsHelper(node, visited, parent, lowValue, discoveryTime, articulationPoints, time)

        # Print the atriculation points
        self.printArticulationPoints(articulationPoints)
    
    # articulation points helper function. A variation of DFS
    def articulationPointsHelper(self, u, visited, parent, lowValue, discoveryTime, articulationPoints, time):
        numberOfChildren = 0
        visited[u] = True
        discoveryTime[u] = time
        lowValue[u] = time
        time += 1

        for v in self.adjacencyList[u]:
            if visited[v] == False:
                numberOfChildren += 1
                parent[v] = u
                self.articulationPointsHelper(v, visited, parent, lowValue, discoveryTime, articulationPoints, time)

                # Updating low value of u for back edge
                lowValue[u] = min(lowValue[u], lowValue[v])

                # Check if the subtree rooted with v has a connection to one of the ancestors of u
                if parent[u] == None and numberOfChildren > 1:
                    articulationPoints[u] += 1
                
                # If u is not root and low value of one of its child is more than discovery value of u
                if parent[u] != None and lowValue[v] >= discoveryTime[u]:
                    articulationPoints[u] += 1
            # Found a cycle
            elif v != parent[u]:
                lowValue[u] = min(lowValue[u], discoveryTime[v])

    
    def reducer(self):
        currentKey = None
        destinationNode = None
        for line in sys.stdin:
            
            src, dest = line.strip().split("\t")

            src = int(src)
            
            # If current iteration is first iteration
            if currentKey is None:
                currentKey = src
                destinationNode = dest
                continue

            # If current iteration is not first iteration and current entry is same as previous entry
            if currentKey == src:
                destinationNode += ","+str(dest)
                continue

            self.createAdjacencyList(currentKey, destinationNode)
            currentKey = src
            destinationNode = dest

        # For the last node
        self.createAdjacencyList(currentKey, destinationNode)

        # Find atriculation points
        self.findArticulationPoints()

if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()

    # reducerObj.adjacencyList = {
    #     1: [0],
    #     0: [2, 3],
    #     2: [1],
    #     3: [4],
    #     4: []
    # }
    # 9+16+13+7+9+9+10+8+7+10 = 98
    # 16 + 13 + 10 + 10 = 49