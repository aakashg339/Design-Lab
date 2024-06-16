# Count the frequency of each edge pair
# Read data from day1.txt, day2.txt, day3.txt, day4.txt, day5.txt, day6.txt, day7.txt, day8.txt, day9.txt, day10.txt
# For each edge, count the frequency of the edge

# Import the required libraries
import os
import re
import sys

# Function to check the edges
def checkEdges(file):
    # Open the file
    with open(file, 'r') as f:
        # Read the file
        lines = f.readlines()
        # Create a set to store the edges
        edges = list()
        # Iterate through the lines
        for line in lines:
            # Split the line to get the edges
            edge = line.strip().split(",")
            # Add the edge to the set
            edges.append((edge[0], edge[1]))
        # Return the set
        return edges

# Get the current directory
currentDirectory = os.getcwd()
# Get the files in the directory
files = os.listdir(currentDirectory)
# Create a set to store the edges
edges = list()
# Iterate through the files
for file in files:
    # Check if the file is a text file
    if file.endswith('.txt'):
        # Get the edges from the file
        fileEdges = checkEdges(file)
        # If the set is empty then add the edges to the set
        if len(edges) == 0:
            edges = fileEdges
        else:
            # add the edges to the list
            edges = edges + list(fileEdges)
        
# Create a dictionary to store the frequency of the edges
edgeFreq = dict()
# Iterate through the edges
for edge in edges:
    # If the edge is already present in the dictionary then increment the frequency
    if edge in edgeFreq:
        edgeFreq[edge] += 1
    # If the edge is not present in the dictionary then add the edge to the dictionary
    else:
        edgeFreq[edge] = 1

# Write the frequency of the edges in descending order as per the frequency, in file edgeFreq.txt
with open("edgeFreq.txt", "w") as f:
    for key, value in sorted(edgeFreq.items(), key=lambda item: item[1], reverse=True):
        f.write("%s\t%s\n" % (key, value))
