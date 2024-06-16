import sys

# Use to count top 10 users with most friends
class Mapper:
    def __init__(self):
        pass

    def mapper(self):
        for line in sys.stdin:
            u, v = line.strip().split(",")

            # Undirected graph so printing both u,v and v,u
            print("{}\t{}".format(u, v))
            print("{}\t{}".format(v, u))
    
if __name__ == "__main__":
    mapperObj = Mapper()
    mapperObj.mapper()