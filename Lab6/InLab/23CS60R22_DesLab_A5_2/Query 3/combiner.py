import sys

# Used to count the number of nodes with degree >= 20
class Combiner:
    def __init__(self):
        pass

    def combiner(self):

        currentKey = None
        hour = 0
        for line in sys.stdin:

            key, value = line.strip().split("\t")
            
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
            print("{}\t{}".format(currentKey, hour))
            currentKey = key
            hour = value
        
        print("{}\t{}".format(currentKey, hour))
                
    
if __name__ == "__main__":
    combinerObj = Combiner()
    combinerObj.combiner()