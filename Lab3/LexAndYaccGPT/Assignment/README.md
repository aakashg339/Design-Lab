# Web Crawling and Extracting Information

Python program to extract information from wikipedia page related to different teams playing Cricket

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
Python program to scrape history and current status related text from pages of teams playing cricket.

### Role of 23CS60R22_CL2_A3_T2.py
Python program to scrape page of a cricket team to get stadium details in their country.

### Role of 23CS60R22_CL2_A3_T3.py
Python program to scrape page of a cricket team to get contracted players details.

### Role of 23CS60R22_CL2_A3_T4.py
Python program to scrape page of a cricket team to get coaching staff details.

### Role of 23CS60R22_CL2_A3_T5.py
Python program to scrape page of a cricket team to get current set of icc rankings of the team.

### Role of 23CS60R22_TS.py
Python program to read text from file 'input.txt', make api call to GPT to summarize the passage, write result in 'output.txt'.

### Role of webpage_download_A.py
Python program to fetch HTML content from wikipedia page of given cricket team country using URL "https://en.wikipedia.org/wiki/"+country+"_national_cricket_team".

### Role of driver.py
Menu driven python program to extract and print the details as per choice.
To get the required data driver.py calls the above files using os library.

## Running it locally on your machine
1. Unzip this repository, and cd to the project root( inside folder 23CS60R22_CL2_A3).
2. Run python3 driver.py

## Purpose
To develop clear idea, how we can use Context Free Grammar to parse web pages