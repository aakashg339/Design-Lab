import sys

# Used to count the number of nodes with degree >= 20
class Combiner:
    def __init__(self):
        pass

    def combiner(self):

        currentKey = None
        currentDatas = None
        for line in sys.stdin:

            key, value = line.strip().split("\t")

            datas = value.strip().split("|")
            
            # If current iteration is first iteration
            if currentKey is None:
                currentKey = key
                currentDatas = value
                continue

            # If current iteration is not first iteration and current node is same as previous node
            if currentKey == key:
                if(datas[3] == '' or datas[4] == '' or datas[5] == '' or datas[6] == ''):
                    currentKey = key
                    currentDatas = value
                continue

            # If a new node is found
            print("{}\t{}".format(currentKey, currentDatas))
            currentKey = key
            currentDatas = value
        
        print("{}\t{}".format(currentKey, currentDatas))
                
    
if __name__ == "__main__":
    combinerObj = Combiner()
    combinerObj.combiner()