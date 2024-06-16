import sys

# Used to get the nodes which are having an edge to any one of the top 10 nodes with maximum frequency
class Mapper:
    def __init__(self):
        self.top10NodeIds = []
        self.top10NodeIdsFilePath = "../Query2/result_2.txt"

    def getTop10NodeIds(self):
        try:
            with open(self.top10NodeIdsFilePath, "r") as f:
                for line in f:
                    nodeId = int(line.strip().split("\t")[0])
                    self.top10NodeIds.append(nodeId)
        except:
            print("Error while reading data from file {}".format(self.top10NodeIdsFilePath))
            exit(1)

    def mapper(self):
        for line in sys.stdin:
            u, v = line.strip().split(",")

            try:
                u = int(u)
                v = int(v)
            except ValueError:
                continue
            
            if u in self.top10NodeIds and v in self.top10NodeIds:
                continue
            if u in self.top10NodeIds:
                print("{}\t1".format(v))
            if v in self.top10NodeIds:
                print("{}\t1".format(u))
    
if __name__ == "__main__":
    mapperObj = Mapper()
    mapperObj.getTop10NodeIds()
    mapperObj.mapper()
