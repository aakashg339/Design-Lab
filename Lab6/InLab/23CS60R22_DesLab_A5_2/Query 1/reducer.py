import sys

# Used to get the nodes which are having an edge to any one of the top 10 nodes with maximum frequency
class Reducer:
    def __init__(self):
        pass

    def reducer(self):
        # variables
        currentKey = None
        currentDatas = None

        # reading lines from console
        for line in sys.stdin:
            key,value = line.strip().split("\t")

            datas = datas = value.strip().split("|")
            
            # If current iteration is first iteration
            if currentKey is None:
                currentKey = key
                currentDatas = datas

            # If current iteration is not first iteration and current node is same as previous node
            if currentKey == key:
                if(datas[3] == '' or datas[4] == '' or datas[5] == '' or datas[6] == ''):
                    currentKey = key
                    currentDatas = datas
                continue

            # If a new node is found
            if(currentDatas[3] == '' or currentDatas[4] == '' or currentDatas[5] == '' or currentDatas[6] == ''):
                print("{}".format(currentKey))
            currentKey = key
            currentDatas = datas

        # If a new node is found
        if(currentDatas[3] == '' or currentDatas[4] == '' or currentDatas[5] == '' or currentDatas[6] == ''):
            print("{}".format(currentKey))


if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()