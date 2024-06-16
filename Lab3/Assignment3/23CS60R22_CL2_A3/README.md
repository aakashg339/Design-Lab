# Web Crawling and Extracting Information

Python program to extract information from wikipedia page related to 2023-2025 Tournament of World Test Championship

This project is part of a Design Lab (CS69202) assignment of IIT Kharagpur. (PDF of the assignment can be found in the repository)

#### Programming Languages Used
* Python

#### Libraries Used
* ply
* os
* urllib
* time
In case of any missing library, kindly install it using 
- pip3 install < library name > (for Python)

### Role of 23CS60R22_CL2_A3_T1.py
Python program to scrape the League Stage results table from https://en.wikipedia.org/wiki/2023%E2%80%932025_ICC_World_Test_Championship

### Role of 23CS60R22_CL2_A3_T2.py
Python program to scrape page of a cricket player from current squad and display details.

### Role of 23CS60R22_CL2_A3_T1_periodicScraper.py
Python program to periodically run webpage_download_A.py and 23CS60R22_CL2_A3_T1.py.

### Role of webpage_download_A.py
Python program to get the HTML data from page https://en.wikipedia.org/wiki/2023%E2%80%932025_ICC_World_Test_Championship

### Role of webpage_download_B.py
Python program to get the HTML data for a player, using url https://en.wikipedia.org/wiki/< player name >

### Role of driver.py
Menu driven python program to extract and print the details as per choice.
To get the required data driver.py calls the above files using os library.

## Running it locally on your machine
1. Unzip this repository, and cd to the project root( inside folder 23CS60R22_CL2_A3).
2. Run python3 driver.py

## Purpose
To develop clear idea, how we can use Context Free Grammar to parse web pages