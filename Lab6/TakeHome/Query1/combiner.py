import sys
import time

# Used agreegate output of mapper and pass to reducer
class Combiner:
    def __init__(self):
        pass

    def combiner(self):

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
            # If the pair of nodes occured atleast 10 times
            print("{}\t{}".format(currentKey, currentFreq))
            currentKey = key
            currentFreq = freq
        
        # For the last node
        print("{}\t{}".format(currentKey, currentFreq))
                
    
if __name__ == "__main__":
    combinerObj = Combiner()
    combinerObj.combiner()