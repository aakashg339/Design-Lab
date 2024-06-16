import sys

# Used to get the nodes which are having an edge to any one of the top 10 nodes with maximum frequency
class Reducer:
    def __init__(self):
        pass

    def reducer(self):
        currentKey = None
        hour = 0
        amount = 0
        for line in sys.stdin:

            key, value = line.strip().split("\t")
            
            key = int(key)
            value = int(value)

            # If current iteration is first iteration
            if currentKey is None:
                currentKey = key
                hour = value
                continue

            # If current iteration is not first iteration and current node is same as previous node
            if currentKey == key:
                hour += value
                continue

            # If a new node is found
            amount += (currentKey * hour)
            currentKey = key
            hour = value
        
        amount += (currentKey * hour)
        print("Total Revenue : {}".format(amount))


if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()