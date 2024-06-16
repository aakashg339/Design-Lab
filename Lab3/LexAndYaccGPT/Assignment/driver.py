# driver file with menu to call other files

import os

def main():
    # Creating log file 'input.log'
    try:
        file_obj = open('input.log', 'w')
        file_obj.close()
    except:
        print("Error. Unable to create input.log")
        return

    while True:
        print("Enter your choice:")
        print("1. Summarize history and current status of the team")
        print("2. International grounds with respective capacity")
        print("3. Set of players in international contract")
        print("4. Set of coatching staff")
        print("5. ICC rankings")
        print("6. Exit")
        choice = int(input())

        # logging the input
        try:
            file_obj = open('input.log', 'a')
            file_obj.write(str(choice) + '\n')
            file_obj.close()
        except:
            print("Error. Unable to write to input.log")
            return

        if choice == 1:
            os.system("python webpage_download_A.py")
            os.system("python 23CS60R22_CL2_A3_T1.py")
            os.system("python 23CS60R22_TS.py")
        elif choice == 2:
            os.system("python webpage_download_A.py")
            os.system("python 23CS60R22_CL2_A3_T2.py")
        elif choice == 3:
            os.system("python webpage_download_A.py")
            os.system("python 23CS60R22_CL2_A3_T3.py")
        elif choice == 4:
            os.system("python webpage_download_A.py")
            os.system("python 23CS60R22_CL2_A3_T4.py")
        elif choice == 5:
            os.system("python webpage_download_A.py")
            os.system("python 23CS60R22_CL2_A3_T5.py")
        elif choice == 6:
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()