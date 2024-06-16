# Approach taken to find attriculation points in the network

## In mapper.py
For each node u,v , passing u,v to STDOUT.

## In combiner.py
Output from mapper.py is sorted and provided as input. Aggregating the output of mapper.py for each file and passing to reducer.py.
For nodes say, u,v and u,w. u\tv,w is passed to reducer.py

## In reducer.py
Output of all the combiner.py is sorted and provided as input. For each node we get the destination nodes and prepare adjacency list from it.
Then implemented Tarjan’s Algorithm to find Strongly Connected Components to get the articulation points.

# Command to spit in parts
split
made makefile commands for k=5, 10, 15, 20 and all nodes to test and prepare report.