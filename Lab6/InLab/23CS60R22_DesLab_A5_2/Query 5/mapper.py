import sys
from datetime import datetime 

# image_regex = re.compile(r'\.(png|jpg|gif|ico)$', re.IGNORECASE)
# video_regex = re.compile(r'\.(mp4|flv)$', re.IGNORECASE)
# audio_regex = re.compile(r'\.(mp3)$', re.IGNORECASE)
# web_regex = re.compile(r'\.(html|css|js|php)$', re.IGNORECASE)

# for line in sys.stdin:
#     fields = line.strip().split()

#     resource = fields[6]
#     res_size = fields[9]

#     if res_size == '-':
#         res_size='0'

#     try:
#         if image_regex.search(resource):
#             print("img\t%s" % (res_size))
#         elif video_regex.search(resource):
#             print("vid\t%s" % (res_size))
#         elif audio_regex.search(resource):
#             print("aud\t%s" % (res_size))
#         elif web_regex.search(resource):
#             print("web\t%s" % (res_size))
#     except Exception as e:
#         # Catch any exceptions that occur while searching for pattern and continue to the next iteration
#         continue
# ride_id, rideable_type, started_at, ended_at, start_station_name, start_station_id, end_station_name, end_station_id, member_casual

import sys

# Used to count the number of nodes with degree >= 20
class Mapper:
    def __init__(self):
        pass

    def mapper(self):

        for line in sys.stdin:
            datas = line.strip().split("\t")

            # Convert the time field into a datetime object
            startTime_obj = datetime.strptime(datas[2], "%Y-%m-%d %H:%M:%S")
            endTime_obj = datetime.strptime(datas[3], "%Y-%m-%d %H:%M:%S") 
            timeDiff = endTime_obj - startTime_obj
            seconds = timeDiff.total_seconds()

            customerId = datas[0]

            if datas[8] == 'casual':
                print("{}\t{}".format(customerId, seconds))
                
    
if __name__ == "__main__":
    mapperObj = Mapper()
    mapperObj.mapper()
