import sys

class Reducer:

    NUM_OF_NUMS = 1000

    def __init__(self):
        pass

    def reducer(self):
        # variables to track current number and its frequency
        freq = [0] * self.NUM_OF_NUMS
        sumN = 0

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
            
            freq[number-1] = count
            sumN+=count


        for i, n in enumerate(freq):
            # print the last remaining number
            print("{}\t{}".format(i+1, n/sumN))

if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()