# Map-Reduce Assignment 1

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
Python program to read file network.txt as u and v.
The data is then passed to STDOUT. Both (u,v) and (v, u) is passed as the graph is undirected.

### Role of reducer.py
Python program to count the nodes which are having >= 20 neighbours. The incomming edges are coming in sorted form as per first column. 
We count the frequency of each node in first column and if frequency >=20 then increasing our count for number of nodes with >= 20 neighbours.

## Query 2
### Role of mapper.py
Python program to read file network.txt as u and v.
The data is then passed to STDOUT. Both (u,v) and (v, u) is passed as the graph is undirected.

### Role of reducer.py
Python program to count top 10 nodes with highest neighbours. The incomming edges are coming in sorted form as per first column. 
We are counting the degree of each node (counting occurance of each node).
If the dictionary of top 10 nodes with highest frequency, is having items < 10, then directly adding to the dictionary. Else finding the key with minimum frequency. If its frequency is less than the current node frequency, then adding the current node in place of key with minimum frequency.

## Query 3
### Role of mapper.py
Python program to read file network.txt as u and v.
If either u or v is present in file with top 10 nodes, then passing it to STDOUT

### Role of reducer.py
Python program to get nodes that are neighbour of top 10 nodes with highest frequency. It reads data from STDIN and prints the unique nodes.
Total users connected to the top 10 nodes were 337 (Ignoring the top 10 nodes).

## Running it locally on your machine
1. Unzip this repository, and cd to the project root( inside folder 23CS60R22).
2. Go inside each query folder.
3. Open terminal and write make

## Purpose
To develop clear idea about Mapper class and Reducer class used in Hardoop