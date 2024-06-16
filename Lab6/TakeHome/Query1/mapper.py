import sys

# Used to read edge and pass a count of 1 for each edge
class Mapper:
    def __init__(self):
        pass

    def mapper(self):

        for line in sys.stdin:
            datas = line.strip().split(",")

            u = int(datas[0])
            v = int(datas[1])

            if u < v:
                print("{},{}\t1".format(u, v))
            else:
                print("{},{}\t1".format(v, u))
    
if __name__ == "__main__":
    mapperObj = Mapper()
    mapperObj.mapper()