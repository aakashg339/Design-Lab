import sys

# Used to get the nodes which are having an edge to any one of the top 10 nodes with maximum frequency
class Reducer:
    def __init__(self):
        pass

    def printNodesWithMaxFreq(self, nodeFreq, maxFreq):
        for node, freq in nodeFreq.items():
            if freq == maxFreq:
                print("{}".format(node))
    
    def reducer(self):
        currentKey = None
        currentFreq = 0
        nodeFreq = {}
        maxFreq = 0
        for line in sys.stdin:
            
            key, freq = line.strip().split("\t")

            freq = int(freq)
            
            # If current iteration is first iteration
            if currentKey is None:
                currentKey = key
                currentFreq = freq
                continue

            # If current iteration is not first iteration and current entry is same as previous entry
            if currentKey == key:
                currentFreq += freq
                continue

            # If a new node is found
            if maxFreq < currentFreq:
                maxFreq = currentFreq
            nodeFreq[currentKey] = currentFreq
            currentKey = key
            currentFreq = freq
        
        # For the last node
        if maxFreq < currentFreq:
            maxFreq = currentFreq
        nodeFreq[currentKey] = currentFreq

        self.printNodesWithMaxFreq(nodeFreq, maxFreq)


if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()
    # 9+16+13+7+9+9+10+8+7+10 = 98
    # 16 + 13 + 10 + 10 = 49