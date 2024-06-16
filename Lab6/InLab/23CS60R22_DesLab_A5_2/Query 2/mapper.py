import sys

# Used to count the number of nodes with degree >= 20
class Mapper:
    def __init__(self):
        pass

    def mapper(self):

        for line in sys.stdin:
            datas = line.strip().split("\t")

            if datas[8] == 'member':
                print("{}\t1".format(datas[1]))
    
if __name__ == "__main__":
    mapperObj = Mapper()
    mapperObj.mapper()
