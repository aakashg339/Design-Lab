#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <errno.h>

#define MESSAGE_SIZE 2048

#define SERVER_BACKLOG 5

#define MAX_QA 150

#define MESSAGE_END_TRANSFER "MESSAGE_END_TRANSFER"

#define ACK_MESSAGE "SUCCESS"
#define ACK_CLOSE_MESSAGE "ACK_CLOSE"
#define ACK_FILE_ERROR_MESSAGE "ACK_FILE_ERROR"
#define ACK_DIRECTORY_ERROR_MESSAGE "ACK_DIRECTORY_ERROR"
#define ACK_TRANSFER_BEGIN_MESSAGE "ACK_TRANSFER_BEGIN"
#define ACK_LS_ERROR_MESSAGE "ACK_LS_ERROR"
#define ACK_MESSAGE_SEND_TO_CLIENT "ACK_MESSAGE_SEND_TO_CLIENT"

#define ACK_ERROR_CLIENT_NOT_FOUND "ACK_ERROR_CLIENT_NOT_FOUND"

int clientUniqueId = 0;

typedef struct clientDetail {
    int id;
    int socket;
} clientDetail;

// clientDetails list to store details of 5 clients
clientDetail *clientDetails[SERVER_BACKLOG];

// Structure to store questions and answers
typedef struct questionAndAnswer {
    char *question;
    char *answer;
} questionAndAnswer;

// chatbot to store questions and answers. Let the defalut length be 150
typedef struct chatbot {
    questionAndAnswer *qa[150];
    int size;
} chatbot;

// chatbot 
chatbot *cb;

void loadChatbot() {
    FILE *file = fopen("FAQs.txt", "r");
    if (file == NULL) {
        perror("Error in opening file.");
        exit(1);
    }

    cb = (chatbot *)malloc(sizeof(chatbot));
    if (cb == NULL) {
        perror("Memory allocation failed.");
        exit(1);
    }
    cb->size = 0;

    char line[MESSAGE_SIZE];

    while (fgets(line, sizeof(line), file) != NULL) {
        line[strcspn(line, "\n")] = 0;
        char *question = strtok(line, "|||");
        char *answer = strtok(NULL, "|||");

        if (question == NULL || answer == NULL) {
            fprintf(stderr, "Error: Invalid format in file.\n");
            continue;
        }

        if (cb->size >= MAX_QA) {
            break;
        }

        cb->qa[cb->size] = (questionAndAnswer *)malloc(sizeof(questionAndAnswer));
        if (cb->qa[cb->size] == NULL) {
            perror("Memory allocation failed.");
            exit(1);
        }

        cb->qa[cb->size]->question = (char *)malloc(strlen(question) + 1);
        cb->qa[cb->size]->answer = (char *)malloc(strlen(answer) + 1);

        if (cb->qa[cb->size]->question == NULL || cb->qa[cb->size]->answer == NULL) {
            perror("Memory allocation failed.");
            exit(1);
        }

        strcpy(cb->qa[cb->size]->question, question);
        strcpy(cb->qa[cb->size]->answer, answer);

        // printf("Question: %s\n", cb->qa[cb->size]->question);
        // printf("Answer: %s\n", cb->qa[cb->size]->answer);

        cb->size++;
    }

    fclose(file);
}

// Function to send acknowledgement to the client
void sendAcknowledgementToClient(int clientSocket, char *ackMessage) {
    char buffer[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    strcpy(buffer, ackMessage);
    send(clientSocket, buffer, strlen(buffer), 0);
}

// Function to remove leading and trailing spaces and return the string
char *trimString(char *string) {
    int i = 0;
    while (string[i] == ' ') {
        i++;
    }
    string = string + i;
    i = strlen(string) - 1;
    while (string[i] == ' ') {
        i--;
    }
    string[i + 1] = '\0';
    return string;
}

void sendListOfActiveClients(int clientSocket, int clientIndex) {
    int i;
    char buffer[MESSAGE_SIZE];
    char temoBuffer[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    for (i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->id != -1) {
            bzero(temoBuffer, MESSAGE_SIZE);
            if (clientDetails[i]->id != clientDetails[clientIndex]->id) {
                sprintf(temoBuffer, "%d\n", clientDetails[i]->id);
            }
            else {
                sprintf(temoBuffer, "%d (You)\n", clientDetails[i]->id);
            }
            strcat(buffer, temoBuffer);
        }
    }
    // printing active clients
    printf("Active clients: %s\n", buffer);
    sendAcknowledgementToClient(clientSocket, buffer);
}

void chatbotFeature(int clientSocket) {
    char buffer[MESSAGE_SIZE];
    int n;
    int isError = 0;
    while (1) {
        // get the response from the server
        bzero(buffer, MESSAGE_SIZE);
        n = read(clientSocket, buffer, sizeof(buffer));
        if (n < 0) {
            perror("Error in reading from server.");
            exit(1);
        }

        printf("stupidbot> %s\n", buffer);

        if (strcmp(buffer, "Bye! Have a nice day and do not complain about me") == 0) {
            break;
        }

        bzero(buffer, MESSAGE_SIZE);
        printf("user> ");
        fgets(buffer, MESSAGE_SIZE, stdin);
        buffer[strcspn(buffer, "\n")] = 0;
        isError = send(clientSocket, buffer, strlen(buffer), 0);

        if (isError < 0) {
            perror("Error in sending message to server.");
            exit(1);
        }
    }
}

// Function to handle each client connection
int receivePingFromClient(char *message, int clientIndex) {
    int clientSocket = clientDetails[clientIndex]->socket;
    int receiveStatus;
    char buffer[MESSAGE_SIZE];

    // copy the message to buffer
    strcpy(buffer, message);

    // remove leading and trailing spaces
    trimString(buffer);

    // If logout string is received, close the connection
    if (strcmp(buffer, "logout") == 0) {
        printf("Client with id: %d disconnected.\n", clientDetails[clientIndex]->id);
        sendAcknowledgementToClient(clientSocket, ACK_CLOSE_MESSAGE);
        close(clientSocket);
        clientDetails[clientIndex]->id = -1;
        clientDetails[clientIndex]->socket = -1;
        return 0;
    }
    else if (strcmp(buffer, "active") == 0) {
        // send the list of active clients to the client
        printf("Client with id: %d requested for active clients.\n", clientDetails[clientIndex]->id);
        sendListOfActiveClients(clientSocket, clientIndex);
    }
    // command send. Format - send <client id> <message>
    else if (strncmp(buffer, "send", 4) == 0) {
        // get the client id to which message is to be sent
        char *token = strtok(buffer, " ");
        token = strtok(NULL, " ");
        int destinationClientId = atoi(token);
        // get the message to be sent
        token = strtok(NULL, " ");
        char messageToSend[MESSAGE_SIZE];
        bzero(messageToSend, MESSAGE_SIZE);
        while (token != NULL) {
            strcat(messageToSend, token);
            strcat(messageToSend, " ");
            token = strtok(NULL, " ");
        }
        // remove leading and trailing spaces
        trimString(messageToSend);

        // at the beginning add 'sender client id: ' to the message
        char tempMessage[MESSAGE_SIZE];
        bzero(tempMessage, MESSAGE_SIZE);
        sprintf(tempMessage, "Message from client with id: %d: ", clientDetails[clientIndex]->id);
        strcat(tempMessage, messageToSend);
        bzero(messageToSend, MESSAGE_SIZE);
        strcpy(messageToSend, tempMessage);

        // send the message to the client
        int i;
        for (i = 0; i < SERVER_BACKLOG; i++) {
            if (clientDetails[i]->id == destinationClientId) {
                printf("Message from client with id: %d to client with id: %d: %s\n", clientDetails[clientIndex]->id, destinationClientId, messageToSend);
                sendAcknowledgementToClient(clientDetails[i]->socket, messageToSend);
                sendAcknowledgementToClient(clientSocket, ACK_MESSAGE_SEND_TO_CLIENT);
                break;
            }
        }
        if (i == SERVER_BACKLOG) {
            // send the message to the client saying 'client not found'
            bzero(buffer, MESSAGE_SIZE);
            sprintf(buffer, "Message from server. Client with id: %d not found", destinationClientId);
            sendAcknowledgementToClient(clientSocket, buffer);
        }
    }
    // /chatbot login
    else if (strcmp(buffer, "chatbot login") == 0) {
        // send the message to the client saying 'command not supported'
        bzero(buffer, MESSAGE_SIZE);
        sprintf(buffer, "Hi, I am stupid bot, I am able to answer a limited set of your questions");
        sendAcknowledgementToClient(clientSocket, buffer);
        chatbotFeature(clientSocket);
    }
    else {
        // send the message to the client saying 'command not supported'
        bzero(buffer, MESSAGE_SIZE);
        sprintf(buffer, "Message from server. Command not supported");
        sendAcknowledgementToClient(clientSocket, buffer);
    }   

    return 1;
}

// Function to create the server socket
int createServerSocket() {
    int serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0) {
        perror("Error in creating socket");
        exit(1);
    }
    printf("TCP server socket created.\n");

    return serverSocket;
}

// Funtion to assign address to server
void assignAddressToServerSocket(int serverSocket, struct sockaddr_in *serverAddress, char *ipOfServer, int port) {
    memset(serverAddress, '\0', sizeof(*serverAddress));
    serverAddress->sin_family = AF_INET;
    serverAddress->sin_port = htons(port);
    serverAddress->sin_addr.s_addr = inet_addr(ipOfServer);
}

// Function to bind the server socket to the specified IP and port
void bindServerSocket(int serverSocket, struct sockaddr_in *serverAddress, int port) {
    if (bind(serverSocket, (struct sockaddr *)serverAddress, sizeof(*serverAddress)) < 0) {
        perror("Error in binding socket to address");
        exit(1);
    }
    printf("Server socket binded to the port number: %d\n", port);
}

// Function to listen for incoming connections
void listenForIncomingConnections(int serverSocket) {
    listen(serverSocket, SERVER_BACKLOG);
    printf("Listening...\n");
}

// Function to close the server socket and destroy the mutex
void closeServerSocketAndDestroyMutex(int serverSocket) {
    close(serverSocket);
}

// Function to update maxFileDescriptor
int findMaxFileDescriptor(int serverSocketFD) {
    int maxFileDescriptor = serverSocketFD; // Reset to the server socket's FD
    for (int i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->socket != -1 && clientDetails[i]->socket > maxFileDescriptor) {
            maxFileDescriptor = clientDetails[i]->socket; // Find the new maximum
        }
    }
}

void main(int argc, char *argv[]) {

    int serverSocketFD, port, acceptedSocketFD, maxFileDescriptor, i, status;
    struct sockaddr_in serverAddress, clientAddress;

    char buffer[MESSAGE_SIZE];

    // Reading the chatbot questions and answers from the file
    loadChatbot();


    // Reading port from command line arguments
    if (argc != 3) {
        printf("Usage: %s <server_ip> <port>\n", argv[0]);
        exit(1);
    }
    
    char *ipOfServer = argv[1];
    port = atoi(argv[2]);

    // allFileDescriptors will store all the file descriptors
    // readFileDescriptors will store the file descriptors which will be passed to select function
    fd_set allFileDescriptors, readFileDescriptors;

    // Initialize the clientDetails list and fd_sets
    for (i = 0; i < SERVER_BACKLOG; i++) {
        clientDetails[i] = (clientDetail *)malloc(sizeof(clientDetail));
        clientDetails[i]->id = -1;
        clientDetails[i]->socket = -1;
    }
    FD_ZERO(&allFileDescriptors);
    FD_ZERO(&readFileDescriptors);

    // Create the server socket
    serverSocketFD = createServerSocket();

    // Calling setsockopt to reuse the port
    int opt = 1;
    if (setsockopt(serverSocketFD, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("Error in setsockopt");
        exit(1);
    }

    // Assign address to server socket
    assignAddressToServerSocket(serverSocketFD, &serverAddress, ipOfServer, port);

    // Bind the server socket to the specified IP and port
    bindServerSocket(serverSocketFD, &serverAddress, port);

    // Listen for incoming connections
    listenForIncomingConnections(serverSocketFD);

    // Add the server socket to the allFileDescriptors set
    FD_SET(serverSocketFD, &allFileDescriptors);

    // Set the maxFileDescriptor to serverSocketFD
    maxFileDescriptor = serverSocketFD;

    while (1) {
        readFileDescriptors = allFileDescriptors;

        // // displaying fd_set, maxFileDescriptor for debugging
        // printf("maxFileDescriptor: %d\n", maxFileDescriptor);
        // for (i = 0; i < maxFileDescriptor; i++) {
        //     if (FD_ISSET(i, &readFileDescriptors)) {
        //         printf("FD: %d\n", i);
        //     }
        // }

        // Select the file descriptors
        if (select(maxFileDescriptor + 1, &readFileDescriptors, NULL, NULL, NULL) < 0) {
            perror("Error in select");
            exit(1);
        }

        // If server socket is in the readFileDescriptors set, then accept the connection
        if (FD_ISSET(serverSocketFD, &readFileDescriptors)) {
            acceptedSocketFD = accept(serverSocketFD, (struct sockaddr *)&clientAddress, (socklen_t *)&clientAddress);
            if (acceptedSocketFD < 0) {
                perror("Error in accepting connection");
                exit(1);
            }

            // Add the accepted socket to the allFileDescriptors set
            FD_SET(acceptedSocketFD, &allFileDescriptors);

            // Update the maxFileDescriptor
            if (acceptedSocketFD > maxFileDescriptor) {
                maxFileDescriptor = acceptedSocketFD;
            }

            // Find the first empty slot in the clientDetails list
            for (i = 0; i < SERVER_BACKLOG; i++) {
                if (clientDetails[i]->socket == -1) {
                    clientDetails[i]->socket = acceptedSocketFD;
                    clientDetails[i]->id = clientUniqueId++;
                    break;
                }
            }

            printf("Client connected with id: %d\n", clientDetails[i]->id);

            // send connected message to client
            sendAcknowledgementToClient(acceptedSocketFD, "Message from server: Connected to server.");
        }

        // Check for the client sockets in the readFileDescriptors set
        for (i = 0; i < maxFileDescriptor; i++) {
            if (i != serverSocketFD && FD_ISSET(clientDetails[i]->socket, &readFileDescriptors)) {
                bzero(buffer, MESSAGE_SIZE);
                status = recv(clientDetails[i]->socket, buffer, sizeof(buffer), 0);
                if (status <= 0) {
                    perror("Error in receiving message from client");
                    // disconnect the client
                    receivePingFromClient("logout", i);

                    // error handling
                    FD_CLR(clientDetails[i]->socket, &allFileDescriptors);
                    clientDetails[i]->socket = -1;
                    clientDetails[i]->id = -1;
                    maxFileDescriptor = findMaxFileDescriptor(serverSocketFD);

                }
                printf("Message from client with id: %d: %s\n", clientDetails[i]->id, buffer);
                status = receivePingFromClient(buffer, i);
                if (status == 0) {

                    // error handling
                    FD_CLR(clientDetails[i]->socket, &allFileDescriptors);
                    clientDetails[i]->socket = -1;
                    clientDetails[i]->id = -1;
                    maxFileDescriptor = findMaxFileDescriptor(serverSocketFD);
                }
            }
        }
    }
}