import sys

class Reducer:
    def __init__(self):
        pass

    def reducer(self):
        # variables to track current number and its frequency
        current_number = -1
        first_count = -1
        modeList = []

        # reading lines from console
        for line in sys.stdin:
            try:
                number, count = line.strip().split("\t")
            except:
                continue

            try:
                number=int(number)
                count=int(count)
            except ValueError:
                continue

            # if we get a new number then first print the current number with its count
            # and then update current_number with the recently scanned number
            if first_count == -1:
                first_count = count
            
            if count == first_count:
                modeList.append(number)
            else:
                break

        # print the last remaining number
        print("Mode List =\t{}".format(modeList))

if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()