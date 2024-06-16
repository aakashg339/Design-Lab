import sys

# Use to count top 10 users with most friends
class Reducer:
    def __init__(self):
        pass

    def maintainTop10List(self, top10NodesWithMaxFreq, currentNode, freq):
        # If map has less than 10 elements
        if len(top10NodesWithMaxFreq) < 10:
            top10NodesWithMaxFreq[currentNode] = freq
        else:
            # Find key with minimum frequency
            minFreqInDict = min(top10NodesWithMaxFreq.values())
            minFreqInDictKey = None
            for key, value in top10NodesWithMaxFreq.items():
                if value == minFreqInDict:
                    minFreqInDictKey = key
                    break
            
            # If the current node has a value more than the minimum frequency
            if freq > minFreqInDict:
                del top10NodesWithMaxFreq[minFreqInDictKey]
                top10NodesWithMaxFreq[currentNode] = freq

    def reducer(self):
        # variables
        currentU = None
        freq = 0
        top10NodesWithMaxFreq = {}

        # reading lines from console
        for line in sys.stdin:
            try:
                u, v = line.strip().split("\t")
            except:
                continue

            try:
                u=int(u)
                v=int(v)
            except ValueError:
                continue
            
            # For first iteration
            if currentU is None:
                currentU = u
                freq = 1
                continue

            # If current node is same as previous node
            if currentU == u:
                freq += 1
                continue

            # If current node is different from previous node
            self.maintainTop10List(top10NodesWithMaxFreq, currentU, freq)

            # As new node is found
            currentU = u
            freq = 1

        # For the last node
        self.maintainTop10List(top10NodesWithMaxFreq, currentU, freq)

        # Printing top10NodesWithMaxFreq
        for key, value in top10NodesWithMaxFreq.items():
            print("{}\t{}".format(key, value))

if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()