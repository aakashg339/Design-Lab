# Approach taken to find nodes which has chatted most with other nodes in the network

## In mapper.py
For each node u,v , passing u\t1 and v\t1. In chat u and v chatter among themself, so passing 1 for both.

## In combiner.py
Output from mapper.py is sortd and provided as input. Aggregating the output of mapper.py for each file and passing to reducer.py

## In reducer.py
Output of all the combiner.py is sorted and provided as input. For each node we then count the frequency and store in dictionary. 
Also simultaniously updating the max value.
Then checking which node has the max value and printing those values.

# Command to spit in parts
split
made makefile commands for k=5, 10, 15, 20 and all nodes to test and prepare report.