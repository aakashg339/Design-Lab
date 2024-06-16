# driver program with menu
import os

data_Dictionary = {}

def prepareData():
    global data_Dictionary

    # Data seperated by '|' and taken from file 'parsedData.txt' where,
    # 1st cell is key
    # 2nd cell is date
    # 3rd cell is details
    # 4th cell is result
    try:
        file_obj = open('parsedData.txt', 'r')
        for line in file_obj:
            data = line.split('|')
            # There can be multiple matches between two countries. Store all the matches in a list
            if data[0] in data_Dictionary:
                data_Dictionary[data[0]].append([data[1], data[2], data[3]])
            else:
                data_Dictionary[data[0]] = [[data[1], data[2], data[3]]]
        file_obj.close()
    except:
        pass
    
# Menu with logger which logs the input from the user
def menu():
    global data_Dictionary

    # Creating the log file
    try:
        file_obj = open('logger.log', 'w')
        file_obj.close()
    except:
        print("Error opening file 'logger.log'")

    # map to store choice and corresponding function
    choice_map = {
        1: 'Get match details',
        2: 'Get player details',
        3: 'Exit'
    }

    # Starting '23CS60R22_CL2_A3_T1_periodicScraper.py' which executed parallely to scrape data from the website and write to file 'webpage.html'
    os.system('python3 23CS60R22_CL2_A3_T1_periodicScraper.py&')

    while True:
        print("----------------------------------------")
        print("1. Get match details")
        print("2. Get player details")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        # Logging the input from the user
        try:
            file_obj = open('logger.log', 'a')
            file_obj.write(choice_map[choice] + '\n')
            file_obj.close()
        except:
            print("Error opening file 'logger.log'")

        if choice == 1:
            # Calling prepareData() every time to get latest data
            prepareData()

            country1 = input("Enter country1: ")
            country2 = input("Enter country2: ")
            key = country1.strip() + " v " + country2.strip()
            if key in data_Dictionary:
                # As there can be multple matches between two countries, print all the matches
                for i, match in enumerate(data_Dictionary[key]):
                    print("Match " + str(i+1) + ":")
                    print("Date: " + match[0])
                    print("Details: " + match[1])
                    print("Result: " + match[2])
            else:
                print("No match found")
        elif choice == 2:
            # Calling 'webpage_download_B.py' to get the HTML data of the player
            os.system("python3 webpage_download_B.py")
            # Calling '23CS60R22_CL2_A3_T2.py' to parse the HTML file and print data
            os.system("python3 23CS60R22_CL2_A3_T2.py")
        elif choice == 3:
            break
        else:
            print("Invalid choice")

# Main method
def main():
    menu()

if __name__ == "__main__":
    main()