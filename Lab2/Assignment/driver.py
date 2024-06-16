# Python program to run 'webpage_download_A.py' and wait for it to finish. Then run '23CS60R22_DesLab_T2_A.py' and wait for it to finish.

import os
import subprocess

# Run 'webpage_download_A.py' and wait for it to finish.
#subprocess.run(['python3', 'webpage_download_A.py'])
# os.system('python3 scraper.py')
data_Dictionary = {}

def prepareDataForSectionThree():
    global data_Dictionary

    # Getting the countries pages
    os.system('python3 webpage_download_C.py')

    # Getting the flag bearer information
    os.system('python3 23CS60R22_DesLab_T2_C2.py')

    # Getting multiple meadle information
    os.system('python3 23CS60R22_DesLab_T2_C3.py')

    # Reading the files to get the data
    # Data stored in map format where key is country name and value is a list of data
    # Reading 'medalData.txt' to get the medal data. Format of file - CountryName:Rank,Gold,Silver,Bronze,Total
    try:
        file_obj = open('medalData.txt','r',encoding="utf-8")
        for line in file_obj:
            line = line.strip()
            line = line.split(':')
            values = line[1].split(',')
            data_Dictionary[line[0]] = {'Rank':values[0], 'Gold':values[1], 'Silver':values[2], 'Bronze':values[3], 'Total':values[4]}
    except:
        print("Not able to read data from file medalData.txt")
        return
    
    # Reading 'flagBearer.txt' to get the flag bearer data. Format of file - CountryName:<Flag bearers (opening)>,<Flag bearers (opening)>,<Flag bearers (closing)>
    try:
        file_obj = open('flagBearer.txt','r',encoding="utf-8")
        for line in file_obj:
            line = line.strip()
            line = line.split(':')
            values = line[1].split(',')
            data_Dictionary[line[0]]['Flag bearers (opening)'] = [values[0], values[1]]
            data_Dictionary[line[0]]['Flag bearers (closing)'] = [values[2]]
    except:
        print("Not able to read data from file flagBearer.txt")
        return

    # Reading 'multipleMedalWinner.txt' to get the multiple medal winner data. Format of file - CountryName:<Name>,<Sports>|<Name>,<Sports>|<Name>,<Sports>,....
    try:
        file_obj = open('multipleMedalWinner.txt','r',encoding="utf-8")
        for line in file_obj:
            line = line.strip()
            line = line.split(':')
            values = line[1].split('|')
            data_Dictionary[line[0]]['Multiple medal winner'] = []
            for value in values:
                # Check if the value is empty or not
                if value == '':
                    continue
                value = value.split(',')
                data_Dictionary[line[0]]['Multiple medal winner'].append([value[0], value[1]])
    except:
        print("Not able to read data from file multipleMedalWinner.txt")
        return

def medalTableSubMenu():
    # iii)For any given country name out of top 10 countries in medal tally print:
    # i) Flag Bearer(opening)
    # ii)Flag Bearer (closing)iii) Multiple Medallist Names and their sport(if any)
    # iv) Given two country names(only for top 10 countries in medal tally):
    # a. Compare their medal tally

    while True:
        print("Sub Menu for medal table")
        print("Press 1 to get flag bearer information")
        print("Press 2 to get multiple medal winner information")
        print("Press 3 to compare two countries")
        print("Press 4 to see country list")
        print("Press 5 to exit")
        choice = int(input())
        if choice == 1:
            print("Enter the name of the country : ", end="")
            country = input()
            # Checking if the country is present in the dictionary
            if country not in data_Dictionary.keys():
                print("Invalid country name")
                continue
            print("Flag bearer (opening): ", data_Dictionary[country]['Flag bearers (opening)'][0], ",", data_Dictionary[country]['Flag bearers (opening)'][1])
            print("Flag bearer (closing): ", data_Dictionary[country]['Flag bearers (closing)'][0])
        elif choice == 2:
            print("Enter the name of the country : ", end="")
            country = input()
            # Checking if the country is present in the dictionary
            if country not in data_Dictionary.keys():
                print("Invalid country name")
                continue

            # Checking whether the country has multiple medal winner or not, by checking the length of the list
            if len(data_Dictionary[country]['Multiple medal winner']) == 0:
                print("No multiple medal winner")
                continue

            print("Multiple medal winner: ")
            for i, value in enumerate(data_Dictionary[country]['Multiple medal winner']):
                print(i+1, ". ", value[0], "(", value[1], ")")
        elif choice == 3:
            print("Enter the name of the first country")
            country1 = input()
            print("Enter the name of the second country")
            country2 = input()

            # Checking if the countries are present in the dictionary
            if country1 not in data_Dictionary.keys() or country2 not in data_Dictionary.keys():
                print("Invalid country name")
                continue

            # Comparing the two countries based on the number of gold medals
            if int(data_Dictionary[country1]['Gold']) > int(data_Dictionary[country2]['Gold']):
                print(country1, " has won more gold medals(", data_Dictionary[country1]['Gold'] ,") than ", country2, "(", data_Dictionary[country2]['Gold'], ")")
            elif int(data_Dictionary[country1]['Gold']) < int(data_Dictionary[country2]['Gold']):
                print(country2, " has won more gold medals(", data_Dictionary[country2]['Gold'] ,") than ", country1, "(", data_Dictionary[country1]['Gold'], ")")
            else:
                print(country1, " and ", country2, " have won equal number of gold medals(", data_Dictionary[country1]['Gold'] ,")")
            
            # Comparing the two countries based on the number of silver medals
            if int(data_Dictionary[country1]['Silver']) > int(data_Dictionary[country2]['Silver']):
                print(country1, " has won more silver medals(", data_Dictionary[country1]['Silver'] ,") than ", country2, "(", data_Dictionary[country2]['Silver'], ")")
            elif int(data_Dictionary[country1]['Silver']) < int(data_Dictionary[country2]['Silver']):
                print(country2, " has won more silver medals(", data_Dictionary[country2]['Silver'] ,") than ", country1, "(", data_Dictionary[country1]['Silver'], ")")
            else:
                print(country1, " and ", country2, " have won equal number of silver medals(", data_Dictionary[country1]['Silver'] ,")")

            # Comparing the two countries based on the number of bronze medals
            if int(data_Dictionary[country1]['Bronze']) > int(data_Dictionary[country2]['Bronze']):
                print(country1, " has won more bronze medals(", data_Dictionary[country1]['Bronze'] ,") than ", country2, "(", data_Dictionary[country2]['Bronze'], ")")
            elif int(data_Dictionary[country1]['Bronze']) < int(data_Dictionary[country2]['Bronze']):
                print(country2, " has won more bronze medals(", data_Dictionary[country2]['Bronze'] ,") than ", country1, "(", data_Dictionary[country1]['Bronze'], ")")
            else:
                print(country1, " and ", country2, " have won equal number of bronze medals(", data_Dictionary[country1]['Bronze'] ,")")
        elif choice == 4:
            print("Country list")
            for key in data_Dictionary.keys():
                print(key)
        elif choice == 5:
            break
        else:
            print("Invalid choice")
            continue

def menu():
    while True:
        print("----------------------------------------------------------------------------------------------------------------")
        print("Main Menu")
        print("Press 1 to 2020 Summer Olympics data for the fields Host city, Motto, Nations, Athletes, Events, Opening, Closing")
        print("Press 2 extract 2020 Summer Olympic Sports program data for 5 sports")
        print("Press 3 for Medal table")
        print("Press 4 to exit")
        choice = int(input())
        if choice == 1:
            print("Wait for few seconds. Processing the data...")

            # Getting the main page '2020 Summer Olympics'
            os.system('python3 webpage_download_A.py')

            # Parse the table to get the data of top ten countries
            os.system('python3 23CS60R22_DesLab_T2_A.py')

            print("--------------------------------Done-----------------------")
        elif choice == 2:
            print("Wait for few seconds. Processing the data...")

            # Getting the webpages of five sports
            os.system('python3 webpage_download_B.py')

            # Parse the table to get the data of five sports
            os.system('python3 23CS60R22_DesLab_T2_B.py')

            print("--------------------------------Done-----------------------")
        elif choice == 3:
            print("Wait for few seconds. Processing the data...")

            # Getting the main page '2020 Summer Olympics'
            os.system('python3 webpage_download_A.py')

            # Parse the table to get the data of top ten countries
            os.system('python3 23CS60R22_DesLab_T2_C1.py')

            # prepare data for menu if dictionary is empty
            if len(data_Dictionary) == 0:
                prepareDataForSectionThree()
            
            # Sub Menu for medal table
            medalTableSubMenu()

            print("--------------------------------Done-----------------------")
        elif choice == 4:
            exit()
        else:
            print("Invalid choice")
            menu()

#########DRIVER FUNCTION#######
def main():
    # Prepare data for section three
    #prepareDataForSectionThree()

    # Menu to call the three files
    menu()

if __name__ == '__main__':
    main()


# print("Press 1 to compare two countries")
#     print("Press 2 to exit")
#     choice = int(input())
#     if choice == 1:
#         print("Enter the name of the first country")
#         country1 = input()
#         print("Enter the name of the second country")
#         country2 = input()

#         # Checking if the countries are present in the dictionary
#         if country1 not in medalDict.keys() or country2 not in medalDict.keys():
#             print("Invalid country name")
#             menu()

#         # Comparing the two countries based on the number of gold medals
#         if medalDict[country1][1] > medalDict[country2][1]:
#             print(country1, " has won more gold medals(", medalDict[country1][1] ,") than ", country2, "(", medalDict[country2][1], ")")
#         elif medalDict[country1][1] < medalDict[country2][1]:
#             print(country2, " has won more gold medals(", medalDict[country2][1] ,") than ", country1, "(", medalDict[country1][1], ")")
#         else:
#             print(country1, " and ", country2, " have won equal number of gold medals(", medalDict[country1][1] ,")")
        
#         # Comparing the two countries based on the number of silver medals
#         if medalDict[country1][2] > medalDict[country2][2]:
#             print(country1, " has won more silver medals(", medalDict[country1][2] ,") than ", country2, "(", medalDict[country2][2], ")")
#         elif medalDict[country1][2] < medalDict[country2][2]:
#             print(country2, " has won more silver medals(", medalDict[country2][2] ,") than ", country1, "(", medalDict[country1][2], ")")
#         else:
#             print(country1, " and ", country2, " have won equal number of silver medals(", medalDict[country1][2] ,")")

#         # Comparing the two countries based on the number of bronze medals
#         if medalDict[country1][3] > medalDict[country2][3]:
#             print(country1, " has won more bronze medals(", medalDict[country1][3] ,") than ", country2, "(", medalDict[country2][3], ")")
#         elif medalDict[country1][3] < medalDict[country2][3]:
#             print(country2, " has won more bronze medals(", medalDict[country2][3] ,") than ", country1, "(", medalDict[country1][3], ")")
#         else:
#             print(country1, " and ", country2, " have won equal number of bronze medals(", medalDict[country1][3] ,")")

#         # Comparing the two countries based on the number of total medals
#         if medalDict[country1][4] > medalDict[country2][4]:
#             print(country1, " has won more total medals(", medalDict[country1][4] ,") than ", country2, "(", medalDict[country2][4], ")")
#         elif medalDict[country1][4] < medalDict[country2][4]:
#             print(country2, " has won more total medals(", medalDict[country2][4] ,") than ", country1, "(", medalDict[country1][4], ")")
#         else:
#             print(country1, " and ", country2, " have won equal number of total medals(", medalDict[country1][4] ,")")
#     elif choice == 2:
#         exit()
#     else:
#         print("Invalid choice")
#         menu()