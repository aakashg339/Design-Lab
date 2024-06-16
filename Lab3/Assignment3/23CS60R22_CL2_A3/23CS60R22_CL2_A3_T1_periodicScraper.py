# Program to periodically scrape the data from the website and print, by calling 23CS60R22_CL2_A3_T1.py
import time
import os

def main():
    while True:
        os.system("python3 webpage_download_A.py")
        os.system("python3 23CS60R22_CL2_A3_T1.py")
        time.sleep(10)

if __name__ == "__main__":
    main()

