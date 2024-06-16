# Finding the edges which is in both directions that is if u-v is present then v-u should also be present
# Read all the files day1.txt, day2.txt, day3.txt, day4.txt, day5.txt, day6.txt, day7.txt, day8.txt, day9.txt, day10.txt and check the edges
# If the edge is present in both the directions then print the edge

import os
import re
import sys

def checkEdges(file):
    # Open the file
    with open(file, 'r') as f:
        # Read the file
        lines = f.readlines()
        # Create a set to store the edges
        edges = set()
        # Iterate through the lines
        for line in lines:
            # Split the line to get the edges
            edge = line.strip().split(",")
            # Add the edge to the set
            edges.add((edge[0], edge[1]))
        # Return the set
        return edges
    
# Get the current directory
currentDirectory = os.getcwd()
# Get the files in the directory
files = os.listdir(currentDirectory)
# Create a set to store the edges
edges = set()
# Iterate through the files
for file in files:
    # Check if the file is a text file
    if file.endswith('.txt'):
        # Get the edges from the file
        fileEdges = checkEdges(file)
        print(file)
        # If the set is empty then add the edges to the set
        if len(edges) == 0:
            edges = fileEdges
        else:
            # Get the intersection of the edges
            edges = edges.union(fileEdges)

# check for each edge if the reverse is present
for edge in edges:
    #print(edge)
    if (edge[1], edge[0]) in edges:
        print(edge)



# Output
# ('u', 'v')
    