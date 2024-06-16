# Assignment 5.2: NoSQL - Mapper, Combiner, Reducer

Python program to implement Map-Reduce to extract relevant information from data.

This project is part of a Design Lab (CS69202) assignment of IIT Kharagpur. (PDF of the assignment can be found in the repository)

#### Programming Languages Used
* Python (Version - 3.8.10)

#### Libraries Used
* sys
In case of any missing library, kindly install it using 
- pip3 install < library name > (for Python)


## Query 1
### Role of mapper.py
Python program to read file event_{}.txt and get the necessary data from it. ride_id is kept as key and rest of columns are combined as single string (seperated by '|' ).

### Role of combiner.py
Collects data from mapper.py and aggregated it. The aggregated data is then passed to reducer.py. If a key has multiple entries and one of them is missing values, then that is passed to reducer.py.

### Role of reducer.py
Python program to collect the data from all the combiner.py and check if the relevant columns are blank or not and display result accordingly.

## Query 2
### Role of mapper.py
Python program to read file event_{}.txt and check if the entry is of member. If so, then pass the bike name with frequency value 1.

### Role of combiner.py
Python program to read and aggregate the output of mapper.py. Here the frequency of bike is being counted for each event file.

### Role of reducer.py
Python program to read and aggregate the output of multiple combiner.py and display the count of each bike.


## Query 3
### Role of mapper.py
Python program to read file event_{}.txt and check if the entry is of member. If so, then pass 5\t1 or pass 10\t1.

### Role of combiner.py
Python program to read and aggregate the output of mapper.py. Here the frequency 5's and 10's are being aggregated.

### Role of reducer.py
Python program to read and aggregate the output of multiple combiner.py and display the amount by calculating the product of hours and 5 or 10 as per the record was for member or casual.


## Query 4
### Role of mapper.py
Python program to read file event_{}.txt and check if the entry is of member. If so, the station name and station ids is passed together as key with value 1.

### Role of combiner.py
Python program to read and aggregate the output of mapper.py. Here the frequency of key (station name|station id) is being counted for each event file.

### Role of reducer.py
Python program to read and aggregate the output of multiple combiner.py. Here the frequency of keys is being calculated and stored in dictionary of size 5. The dictionary is being updated when a new key with more frequency is being found.


## Query 5
### Role of mapper.py
Python program to read file event_{}.txt and check if the entry is of casual type. If so, then pass customer id and duration of rental in seconds .

### Role of combiner.py
Python program to read and aggregate the output of mapper.py. Here the duration for each customer is summed up.

### Role of reducer.py
Python program to read and aggregate the output of multiple combiner.py and display. Here total duration is calculated and also the total number of users. Then the users with duration greater than the average will be displayed.

## Running it locally on your machine
1. Unzip this repository, and cd to the project root( inside folder 23CS60R22).
2. Go inside each query folder.
3. Open terminal and write make

## Purpose
To develop clear idea about Mapper class and Reducer class used in Hardoop