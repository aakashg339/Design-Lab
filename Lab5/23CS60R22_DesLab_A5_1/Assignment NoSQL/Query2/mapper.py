import sys

class Mapper:
    def __init__(self):
        pass
    
    def map(self):
        for line in sys.stdin:
            number = line.strip()
            print("{}".format(number))
    
if __name__ == "__main__":
    mapperObj = Mapper()
    mapperObj.map()