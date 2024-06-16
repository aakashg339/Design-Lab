import sys

# Used to get the nodes which are having an edge to any one of the top 10 nodes with maximum frequency
class Reducer:
    def __init__(self):
        pass

    def reducer(self):
        currentKey = None
        freq = 0
        for line in sys.stdin:

            key, value = line.strip().split("\t")

            value = int(value)
            
            # If current iteration is first iteration
            if currentKey is None:
                currentKey = key
                freq = value
                continue

            # If current iteration is not first iteration and current node is same as previous node
            if currentKey == key:
                freq += value
                continue

            # If a new node is found
            print("{}\t{}".format(currentKey, freq))
            currentKey = key
            freq = value
        
        print("{}\t{}".format(currentKey, freq))


if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()