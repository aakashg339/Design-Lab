import sys

# Used to read edge and pass a count of 1 for each edge
class Mapper:
    def __init__(self):
        pass

    def mapper(self):

        for line in sys.stdin:
            datas = line.strip().split(",")
            print("{},{}".format(datas[0], datas[1]))
    
if __name__ == "__main__":
    mapperObj = Mapper()
    mapperObj.mapper()
