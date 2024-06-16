import sys

class Reducer:
    def __init__(self):
        pass

    def reducer(self):
        # variables to track number and its frequency
        current_number = -1
        current_count = 0 

        # reading lines from console
        for line in sys.stdin:
            try:
                number, count = line.strip().split("\t")
            except:
                continue

            try:
                count=int(count)
            except ValueError:
                continue

            # if we get a new number then first print the current number with its count
            # and then update number with the recently scanned number
            if current_number != number:
                if current_number != -1:
                    print("{}\t{}".format(current_number,current_count))
                current_number = number
                current_count=0
            # increment the frequency of current ip
            current_count += count

        # print the last remaining number
        print("{}\t{}".format(current_number,current_count))

if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()
