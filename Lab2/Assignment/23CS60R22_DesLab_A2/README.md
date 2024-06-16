# Web Crawling and Extracting Information

Python program to extract information from https://en.wikipedia.org/wiki/2020_Summer_Olympics

This project is part of a Design Lab (CS69202) assignment of IIT Kharagpur. (PDF of the assignment can be found in the repository)

#### Programming Languages Used
* Python

#### Libraries Used
* ply
* os
* urllib
In case of any missing library, kindly install it using 
- pip3 install < library name > (for Python)

### Role of 23CS60R22_DesLab_T2_A.py
Python program to parse and get Host city, Motto, Nations, Athletes, Events, Opening, Closing from https://en.wikipedia.org/wiki/2020_Summer_Olympics

### Role of 23CS60R22_DesLab_T2_B.py
Python program to parse and get any five sports details

### Role of 23CS60R22_DesLab_T2_C1.py
Python program to parse the Medal Table.

### Role of 23CS60R22_DesLab_T2_C2.py
Python program to parse the Opening and Closing flag bearer data.

### Role of 23CS60R22_DesLab_T2_C3.py
Python program to parse the multiple medals list data

### Role of webpage_download_A.py
Python program to get HTML data of page https://en.wikipedia.org/wiki/2020_Summer_Olympics

### Role of webpage_download_B.py
Python program to get HTML data of any five sports

### Role of webpage_download_C.py
Python program to get HTML data of countries participating in the Olympics

### Role of driver.py
Menu driven python program to extract and print the details of three table as mentioned in assignment.
To get the required data driver.py calls the above files using os library.

## Running it locally on your machine
1. Unzip this repository, and cd to the project root( inside folder 23CS60R22_DesLab_A2).
2. Run python3 driver.py

## Purpose
To develop clear idea, how we can use Context Free Grammar to parse web pages