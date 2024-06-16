import sys
import time

# Used agreegate output of mapper and pass to reducer
class Combiner:
    def __init__(self):
        pass

    def combiner(self):

        currentKey = None
        destinationNode = None
        for line in sys.stdin:
            
            src, dest = line.strip().split(",")

            src = int(src)
            dest = dest
            
            # If current iteration is first iteration
            if currentKey is None:
                currentKey = src
                destinationNode = dest
                continue

            # If current iteration is not first iteration and current entry is same as previous entry
            if currentKey == src:
                destinationNode += ","+str(dest)
                continue

            # If a new node is found
            # If the pair of nodes occured atleast 10 times
            print("{}\t{}".format(currentKey, destinationNode))
            currentKey = src
            destinationNode = dest
        
        # For the last node
        print("{}\t{}".format(currentKey, destinationNode))
                
    
if __name__ == "__main__":
    combinerObj = Combiner()
    combinerObj.combiner()