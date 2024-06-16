# Client-Server Chat Application with FAQ Chatbot (Part - 1)

C program to implement client server chat application.

This project is part of a Design Lab (CS69202) assignment of IIT Kharagpur. (PDF of the assignment can be found in the repository)

#### Programming Languages Used
* C

#### Libraries Used
* stdio
* stdlib
* string
* unistd.h
* arpa/inet.h
* sys/signal.h
* netdb.h
* netinet/in.h
* sys/socket.h
* sys/types.h
* sys/time.h
In case of any missing library, kindly install it.

## Query 1
### Role of chatServer.c
To habdle requests from the client.

### Role of chatClient.c
To communicate with server and with other clients.

### Assumptions
- Converting every string to lower case. Both /active and /ActIve will be treated same.

## Running it locally on your machine
1. Unzip this repository, and cd to the project root( inside folder 23CS60R22_FAQ_D1).
2. For server
- To compile - gcc chatServer.c -o server
- To run - ./server < valid port number >                              Ex - ./server 5000
3. For client
- To compile - gcc chatClient.c -o client
- To run - ./client 127.0.0.1 < port number same as server >           Ex - ./client 127.0.0.1 5000
4. First start server then then client

## Purpose
To develop clear idea client server chat application.