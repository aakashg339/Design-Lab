import sys
from datetime import datetime 

import sys

# Used to count the number of nodes with degree >= 20
class Mapper:
    def __init__(self):
        pass

    def mapper(self):

        for line in sys.stdin:
            datas = line.strip().split("\t")

            hour = 0
            # Convert the time field into a datetime object
            startTime_obj = datetime.strptime(datas[2], "%Y-%m-%d %H:%M:%S")
            endTime_obj = datetime.strptime(datas[3], "%Y-%m-%d %H:%M:%S") 
            timeDiff = endTime_obj - startTime_obj
            seconds = timeDiff.total_seconds()

            hour = int((seconds / (60 * 60)))
            if(seconds % (60 * 60) != 0):
                hour = hour + 1

            if datas[8] == 'member':
                print("{}\t{}".format(5, hour))
            if datas[8] == 'casual':
                print("{}\t{}".format(10, hour))
    
if __name__ == "__main__":
    mapperObj = Mapper()
    mapperObj.mapper()
