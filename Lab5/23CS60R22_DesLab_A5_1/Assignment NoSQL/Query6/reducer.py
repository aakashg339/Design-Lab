import sys

class Reducer:
    def __init__(self):
        pass

    def reduce(self):
        # variables to track current number and its frequency
        numberList = []

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

            for i in range(1, count+1):
                numberList.append(number)

        # 
        index = []
        median = 0
        if len(numberList) % 2 != 1:
            index1 = int((len(numberList) + 1) / 2)
            index.append(index1-1)
        else:
            index1 = int((len(numberList)) / 2)
            index2 = index1 + 1
            index.append(index1-1)
            index.append(index2-1)

        # Getting median
        for n in index :
            median += numberList[n]
        median /= len(index)

        # print the last remaining number
        print("Median =\t{}".format(median))

if __name__ == "__main__":
    reducer_obj = Reducer()
    reducer_obj.reduce()