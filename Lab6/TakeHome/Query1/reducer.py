import sys

# Used to agreegate output of combiner and print the edges whose frequency is greater than or equal to 10
class Reducer:
    def __init__(self):
        pass

    def reducer(self):
        currentKey = None
        currentFreq = None
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
            nodes = currentKey.split(",")
            # Display only if the pair of nodes occured atleast 10 times
            if currentFreq >= 10:
                print("{},{}".format(nodes[0], nodes[1]))
            currentKey = key
            currentFreq = freq
        
        # For the last node
        nodes = currentKey.split(",")
        if currentFreq >= 10:
            print("{},{}".format(nodes[0], nodes[1]))


if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()
    # 9+16+13+7+9+9+10+8+7+10 = 98
    # 16 + 13 + 10 + 10 = 49