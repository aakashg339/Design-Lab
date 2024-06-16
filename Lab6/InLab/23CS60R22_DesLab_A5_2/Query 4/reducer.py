import sys

# Used to get the nodes which are having an edge to any one of the top 10 nodes with maximum frequency
class Reducer:
    def __init__(self):
        pass

    def updateTop5(self, top5, key, value):
        if len(top5) < 5:
            top5[key] = value
        else:
            currentMinValue = min(top5.values())
            if value > currentMinValue:
                # The the key with minimum value
                for k, v in top5.items():
                    if v == currentMinValue:
                        break
                top5.pop(k)
                top5[key] = value
    
    def reducer(self):
        currentKey = None
        freq = 0
        top5 = {}
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
            self.updateTop5(top5, currentKey, freq)
            currentKey = key
            freq = value
        
        # For the last node
        self.updateTop5(top5, currentKey, freq)
        for k, v in top5.items():
            # Split key by |
            start_name, start_id = k.split("|")
            print("{} , {}".format(start_name, start_id))


if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()