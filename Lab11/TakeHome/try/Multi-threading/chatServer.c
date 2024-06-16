#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>

#define MESSAGE_SIZE 1024

#define SERVER_BACKLOG 10

#define MAX_QA 150

#define MESSAGE_END_TRANSFER "MESSAGE_END_TRANSFER"

#define ACK_MESSAGE "SUCCESS"
#define ACK_CLOSE_MESSAGE "ACK_CLOSE"
#define ACK_FILE_ERROR_MESSAGE "ACK_FILE_ERROR"
#define ACK_DIRECTORY_ERROR_MESSAGE "ACK_DIRECTORY_ERROR"
#define ACK_TRANSFER_BEGIN_MESSAGE "ACK_TRANSFER_BEGIN"
#define ACK_LS_ERROR_MESSAGE "ACK_LS_ERROR"
#define ACK_INVALID_COMMAND_MESSAGE "ACK_INVALID_COMMAND"
#define ACK_CLIENT_DISCONNECTED_MESSAGE "ACK_CLIENT_DISCONNECTED"

pthread_mutex_t mutex;

// Structure to store the client details
typedef struct clientDetail {
    int id;
    int socket;
} clientDetail;

// clientDetails list to store details of 5 clients
clientDetail *clientDetails[SERVER_BACKLOG];
int clientCount;

// Structure to store questions and answers
typedef struct questionAndAnswer {
    char *question;
    char *answer;
} questionAndAnswer;

// chatbot to store questions and answers. Let the defalut length be 150
typedef struct chatbot {
    questionAndAnswer *qa[MAX_QA];
    int size;
} chatbot;

// chatbot 
chatbot *cb;

// Function to initialize the client details
void initializeClientDetailsAndChatBot() {
    int i;

    for (i = 0; i < SERVER_BACKLOG; i++) {
        clientDetails[i] = (clientDetail *)malloc(sizeof(clientDetail));
        clientDetails[i]->id = -1;
        clientDetails[i]->socket = -1;
    }
    clientCount = 0;

    cb = (chatbot *)malloc(sizeof(chatbot));
    for (i = 0; i < MAX_QA; i++) {
        cb->qa[i] = (questionAndAnswer *)malloc(sizeof(questionAndAnswer));
        cb->qa[i]->question = (char *)malloc(MESSAGE_SIZE);
        cb->qa[i]->answer = (char *)malloc(MESSAGE_SIZE);
    }

    cb->size = 0;

    printf("Client details initialized.\n");
}

// Function to store the client details
void storeClientDetails(int id, int socket) {
    pthread_mutex_lock(&mutex);
    clientDetails[clientCount]->id = id;
    clientDetails[clientCount]->socket = socket;
    clientCount++;
    pthread_mutex_unlock(&mutex);
    printf("Client %d details stored.\n", id);
}

// Function to remove the client details
void removeClientDetails(int id) {
    pthread_mutex_lock(&mutex);
    for (int i = 0; i < clientCount; i++) {
        if (clientDetails[i]->id == id) {
            clientDetails[i]->id = -1;
            clientDetails[i]->socket = -1;
            break;
        }
    }
    pthread_mutex_unlock(&mutex);
    printf("Client %d details removed.\n", id);
}

// Function to get client ids as a string
char *getClientIds(int clientOwnSocket) {
    pthread_mutex_lock(&mutex);
    char buffer[MESSAGE_SIZE];
    char temp[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    bzero(temp, MESSAGE_SIZE);

    for (int i = 0; i < clientCount; i++) {
        if (clientDetails[i]->id != -1) {
            bzero(temp, MESSAGE_SIZE);
            if(clientDetails[i]->socket == clientOwnSocket) {
                sprintf(temp, "%d (Own)\n", clientDetails[i]->id);
            }
            else {
                sprintf(temp, "%d\n", clientDetails[i]->id);
            
            }
            strcat(buffer, temp);
        }
    }
    
    pthread_mutex_unlock(&mutex);
    return strdup(buffer);
}

// load chatbot data
void loadChatbot() {
    FILE *file = fopen("FAQs.txt", "r");
    if (file == NULL) {
        perror("Error in opening file.");
        exit(1);
    }

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

        if (cb->qa[cb->size] == NULL) {
            perror("Memory allocation failed.");
            exit(1);
        }

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
}

// Function to send acknowledgement to the client
void sendAcknowledgementToClient(int clientSocket, char *ackMessage) {
    char buffer[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    strcpy(buffer, ackMessage);
    printf("Sending acknowledgement to client: %s\n", buffer);
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

// Function to handle each client connection
void *receivePingFromClient(void *args) {
    int clientSocket = *(int *)args, receiveStatus;
    struct sockaddr_in clientAddress;
    socklen_t addressSize = sizeof(clientAddress);
    char buffer[MESSAGE_SIZE];

    // Storing the client details
    int clientId;

    // For client id use random number of 6 digits such that it is unique for each client
    clientId = (clientSocket) % 900000 + 100000;

    storeClientDetails(clientId, clientSocket);


    while (1) {
        bzero(buffer, MESSAGE_SIZE);
        receiveStatus = recv(clientSocket, buffer, sizeof(buffer), 0);

        if (receiveStatus <= 0) {
            continue;
        }

        // If close string is received, close the connection
        if (strcmp(buffer, "/logout") == 0) {
            removeClientDetails(clientId);
            printf("Client disconnected.\n");
            sendAcknowledgementToClient(clientSocket, ACK_CLOSE_MESSAGE);
            break;
        }
        // “/active” - retrieve a list of active clients
        else if (strcmp(buffer, "/active") == 0) {
            char *clientIds = getClientIds(clientSocket);
            send(clientSocket, clientIds, strlen(clientIds), 0);
            free(clientIds);
        }
        // "/send <dest_id> <message>" - send messages to other clients using their unique IDs
        else if (strncmp(buffer, "/send", 5) == 0) {
            char *message = buffer + 6;
            char *destId = strtok(message, " ");
            // remaining part is the message. The message might have spaces so we need to handle it
            char *msg = strtok(NULL, "");
            int destClientId = atoi(destId);
            char *msgToSend = trimString(msg);

            int destClientSocket = -1;
            for (int i = 0; i < clientCount; i++) {
                if (clientDetails[i]->id == destClientId) {
                    destClientSocket = clientDetails[i]->socket;
                    break;
                }
            }

            if (destClientSocket == -1) {
                sendAcknowledgementToClient(clientSocket, ACK_CLIENT_DISCONNECTED_MESSAGE);
            }
            else {
                char messageToSend[MESSAGE_SIZE];
                bzero(messageToSend, MESSAGE_SIZE);
                sprintf(messageToSend, "Message from client %d: %s", clientId, msgToSend);
                send(destClientSocket, messageToSend, strlen(messageToSend), 0);
                sendAcknowledgementToClient(clientSocket, ACK_MESSAGE);
            }
        }
        else{
            printf("Message from client: %s\n", buffer);
            sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND_MESSAGE);
        }

    }

    close(clientSocket);
    free(args);
    return NULL;
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

// Function to initialize the mutex
void initializeMutex() {
    if (pthread_mutex_init(&mutex, NULL) != 0) {
        perror("Error. Could not initialize mutex");
        exit(1);
    }
}

// Function to close the server socket and destroy the mutex
void closeServerSocketAndDestroyMutex(int serverSocket) {
    close(serverSocket);
    pthread_mutex_destroy(&mutex);
}

// Function to accept incoming connections
int acceptIncomingConnections(int serverSocket) {
    int clientSocket;
    struct sockaddr_in clientAddress;
    socklen_t addressSize = sizeof(clientAddress);

    clientSocket = accept(serverSocket, (struct sockaddr *)&clientAddress, &addressSize);
    if (clientSocket < 0) {
        perror("Error. Could not accept connection");
        exit(1);
    }
    printf("Client connected.\n");

    return clientSocket;
}


// Function to accept incoming connections and create a thread for each connection
void acceptIncomingConnectionsAndCreateThread(int serverSocket) {
    int clientSocket;

    while (1) {
        // Accepting incoming connections
        clientSocket = acceptIncomingConnections(serverSocket);

        pthread_t thread_id;
        int *newClientSocket = malloc(1);
        *newClientSocket = clientSocket;

        if (pthread_create(&thread_id, NULL, receivePingFromClient, (void *)newClientSocket) != 0) {
            perror("Error. Could not create thread");
            exit(1);
        }
        pthread_detach(thread_id);
    }

    pthread_exit(NULL);
}

void main(int argc, char *argv[]) {

    int serverSocket, port;
    struct sockaddr_in serverAddress;

    // Reading port from command line arguments
    if (argc != 3) {
        printf("Usage: %s <server_ip> <port>\n", argv[0]);
        exit(1);
    }
    
    char *ipOfServer = argv[1];
    port = atoi(argv[2]);

    // Initializing the mutex
    initializeMutex();

    // Initializing the client details
    initializeClientDetailsAndChatBot();

    // Loading chatbot data
    loadChatbot();

    // Creating the server socket
    serverSocket = createServerSocket();

    // Assigning address to the server socket
    assignAddressToServerSocket(serverSocket, &serverAddress, ipOfServer, port);

    // Binding the server socket to the specified IP and port
    bindServerSocket(serverSocket, &serverAddress, port);

    // Listening for incoming connections
    listenForIncomingConnections(serverSocket);

    // Acccepting incoming connections and creating a thread for each connection
    acceptIncomingConnectionsAndCreateThread(serverSocket);

    // Closing the server socket and destroying the mutex
    closeServerSocketAndDestroyMutex(serverSocket);
}
