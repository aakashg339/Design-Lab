import sys
from datetime import datetime

# Used to count the number of nodes with degree >= 20
class Mapper:
    def __init__(self):
        pass

    def mapper(self):

        for line in sys.stdin:
            datas = line.strip().split("\t")

            if datas[8] != 'member':
                continue

            if datas[4] and datas[4] != '':
                start_station_name = datas[4].strip()
            else:
                continue
            
            if datas[5] and datas[5] != '':
                start_station_id = datas[5].strip()
            else:
                continue

            print("{}|{}\t1".format(start_station_name, start_station_id))
                
    
if __name__ == "__main__":
    mapperObj = Mapper()
    mapperObj.mapper()
