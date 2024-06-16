import sys

# Used to get the nodes which are having an edge to any one of the top 10 nodes with maximum frequency
class Reducer:
    def __init__(self):
        self.adjacencyList = {}

        for i in range(0, 300):
            self.adjacencyList[i] = []
    
    def createAdjacencyList(self, currentKey, destinationNode):
        currentKey = int(currentKey)
        destinationNode = destinationNode.split(",")
        destinationNode = list(map(int, destinationNode))

        for node in destinationNode:
            if node not in self.adjacencyList[currentKey]:
                self.adjacencyList[currentKey].append(node)

    def findEdgesNotInAdjacencyList(self):
        for i in range(0, 300):
            for j in range(i+1, 300):
                if i != j and j not in self.adjacencyList[i]:
                    print(str(i)+","+str(j))
    
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

        # Find edges not in adjacency list
        self.findEdgesNotInAdjacencyList()

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