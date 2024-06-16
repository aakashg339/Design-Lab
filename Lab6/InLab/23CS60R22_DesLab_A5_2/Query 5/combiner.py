import sys

# Used to count the number of nodes with degree >= 20
class Combiner:
    def __init__(self):
        pass

    def combiner(self):

        currentKey = None
        freq = 0
        for line in sys.stdin:

            key, value = line.strip().split("\t")
            
            value = float(value)

            # If current iteration is first iteration
            if currentKey is None:
                currentKey = key
                freq = value
                continue
                #currentDatas = ":".join(datas[3:7])

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
    combinerObj = Combiner()
    combinerObj.combiner()