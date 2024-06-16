import sys

# Used to get the nodes which are having an edge to any one of the top 10 nodes with maximum frequency
class Reducer:
    def __init__(self):
        pass

    def reducer(self):
        # variables
        currentU = None

        # reading lines from console
        for line in sys.stdin:
            try:
                node, c = line.strip().split("\t")
            except:
                continue

            try:
                node=int(node)
            except ValueError:
                continue
            
            # If current iteration is first iteration
            if currentU is None:
                currentU = node
                continue

            # If current iteration is not first iteration and current node is same as previous node
            if currentU == node:
                continue

            # If a new node is found
            print("{}".format(currentU))
            currentU = node

        # For the last unchecked node
        print("{}".format(currentU))


if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()