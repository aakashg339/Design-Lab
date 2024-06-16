import sys

# Used to count the number of nodes with degree >= 20
class Reducer:
    def __init__(self):
        pass

    def reducer(self):
        # variables
        currentU = -1
        freq = 0
        countGreaterThan20 = 0

        # reading lines from console
        for line in sys.stdin:
            try:
                u, v = line.strip().split("\t")
            except:
                continue

            try:
                u=int(u)
                v=int(v)
            except ValueError:
                continue
            
            if currentU != u:
                if currentU != -1 and freq >= 20:
                    countGreaterThan20 = countGreaterThan20 + 1
                currentU = u
                freq = 0
            freq = freq + 1

            # print("{}\t{}".format(u, v))

        # For the last remaining u
        if currentU != -1 and freq >= 20:
            countGreaterThan20 = countGreaterThan20 + 1
        
        print("Number of Users with more than 20 friends = {}".format(countGreaterThan20))
        print("Budget to be allocated = {}".format(countGreaterThan20 * 100))

if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()