import sys

class Reducer:
    def __init__(self):
        pass

    def reducer(self):
        # variables to track current max
        current_max = -1
        number = -1

        # reading lines from console
        for line in sys.stdin:
            try:
                number = line.strip()
            except:
                continue

            try:
                number=int(number)
            except ValueError:
                continue
            
            current_max = number
            break

        # print the maximum number
        print("Largest Number = {}".format(current_max))

if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()

