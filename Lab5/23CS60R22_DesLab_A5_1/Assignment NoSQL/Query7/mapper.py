import sys

class Mapper:
    def __init__(self):
        pass

    def maper(self):
        for line in sys.stdin:
            try:
                number, count = line.strip().split("\t")
            except:
                continue
            
            print("{}\t{}".format(number, count))

if __name__ == "__main__":
    mapperObj = Mapper()
    mapperObj.maper()