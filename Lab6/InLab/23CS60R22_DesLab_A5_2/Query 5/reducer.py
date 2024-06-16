import sys

# Used to get the nodes which are having an edge to any one of the top 10 nodes with maximum frequency
class Reducer:
    def __init__(self):
        pass

    def printUsersWithDurationMoreThanAverage(self, userIdDurationMap, averageDuration):
        for userId, duration in userIdDurationMap.items():
            if duration > averageDuration:
                print("{}".format(userId))
    
    def reducer(self):
        currentKey = None
        freq = 0
        durationSum = 0
        totalUniqueCustomers = 0
        userIdDurationMap = {}
        for line in sys.stdin:

            key, value = line.strip().split("\t")
            
            value = float(value)

            # If current iteration is first iteration
            if currentKey is None:
                currentKey = key
                freq = value
                continue

            # If current iteration is not first iteration and current node is same as previous node
            if currentKey == key:
                freq += value
                continue

            # If a new node is found
            durationSum += freq
            totalUniqueCustomers += 1
            userIdDurationMap[currentKey] = freq
            currentKey = key
            freq = value
        
        # For the last node
        durationSum += freq
        totalUniqueCustomers += 1
        userIdDurationMap[currentKey] = freq

        averageDuration = durationSum / totalUniqueCustomers

        self.printUsersWithDurationMoreThanAverage(userIdDurationMap, averageDuration)


if __name__ == "__main__":
    reducerObj = Reducer()
    reducerObj.reducer()