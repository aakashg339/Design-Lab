import sys

class Reducer:
    def __init__(self):
        pass

    def reducer(self):
        # variables to track number and its frequency
        total_numbers = 0
        total_count = 0

        # reading lines from console
        for line in sys.stdin:
            try:
                number, count = line.strip().split("\t")
            except:
                continue

            try:
                number = int(number)
                count=int(count)
            except ValueError:
                continue

            total_numbers += (number * count)
            total_count += count

        mean = total_numbers / total_count

        # print the last remaining number
        print("Mean = {}".format(mean))
    
if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()