#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define MESSAGE_SIZE 1024

#define SERVER_BACKLOG 5

#define MESSAGE_END_TRANSFER "MESSAGE_END_TRANSFER"

#define ACK_MESSAGE "SUCCESS"
#define ACK_CLOSE_MESSAGE "ACK_CLOSE"
#define ACK_FILE_ERROR_MESSAGE "ACK_FILE_ERROR"
#define ACK_DIRECTORY_ERROR_MESSAGE "ACK_DIRECTORY_ERROR"
#define ACK_TRANSFER_BEGIN_MESSAGE "ACK_TRANSFER_BEGIN"
#define ACK_LS_ERROR_MESSAGE "ACK_LS_ERROR"
#define ACK_MESSAGE_SEND_TO_CLIENT "ACK_MESSAGE_SEND_TO_CLIENT"

#define ACK_ERROR_CLIENT_NOT_FOUND "ACK_ERROR_CLIENT_NOT_FOUND"

#define CLIENT_DETAILS_FILE "clientDetails.log"

int clientUniqueId = 0;

// structure to store client details
typedef struct ClientDetail {
    int uniqueId;
    int port;
    char ip[100];
} ClientDetail;

// structure to store client details
typedef struct ClientDetails {
    ClientDetail clientDetail[100];
    int count;
} ClientDetails;

// Function to clear contents of the file
void clearFile(char *fileName) {
    FILE *filePointer;
    filePointer = fopen(fileName, "w");
    if (filePointer == NULL) {
        perror("Error in opening file");
        exit(1);
    }
    fclose(filePointer);
}

// Function to store the client details in a file. Only store unique id and port number
void storeClientDetailsInFile(int uniqueId, int port, struct sockaddr_in clientAddress) {
    FILE *filePointer;
    filePointer = fopen(CLIENT_DETAILS_FILE, "a");
    if (filePointer == NULL) {
        perror("Error in opening file");
        exit(1);
    }
    fprintf(filePointer, "%d %d %s\n", uniqueId, port, inet_ntoa(clientAddress.sin_addr));
    fclose(filePointer);
}

// Function the read the client details from the file and return the structure
ClientDetails *readClientDetailsFromFile() {
    FILE *filePointer;
    ClientDetails *clientDetails = (ClientDetails *)malloc(sizeof(ClientDetails));
    filePointer = fopen(CLIENT_DETAILS_FILE, "r");
    if (filePointer == NULL) {
        perror("Error in opening file");
        exit(1);
    }
    int uniqueId, port;
    int count = 0;
    // variable for address
    char *ipOfClients = (char *)malloc(100 * sizeof(char));
    while (fscanf(filePointer, "%d %d %s", &uniqueId, &port, ipOfClients) != EOF) {
        clientDetails->clientDetail[count].uniqueId = uniqueId;
        clientDetails->clientDetail[count].port = port;
        strcpy(clientDetails->clientDetail[count].ip, ipOfClients);
        count++;
    }
    clientDetails->count = count;
    fclose(filePointer);
    return clientDetails;
}

// Function to remove the client details from the file, given the unique id
void removeClientDetailsFromFile(int uniqueId) {
    FILE *filePointer;
    filePointer = fopen(CLIENT_DETAILS_FILE, "r");
    if (filePointer == NULL) {
        perror("Error in opening file");
        exit(1);
    }
    FILE *tempFilePointer;
    tempFilePointer = fopen("temp.log", "w");
    if (tempFilePointer == NULL) {
        perror("Error in opening file");
        exit(1);
    }
    int uniqueIdFromFile, port;
    // for address
    char *ipOfClients = (char *)malloc(100 * sizeof(char));
    while (fscanf(filePointer, "%d %d %s", &uniqueIdFromFile, &port, ipOfClients) != EOF) {
        if (uniqueIdFromFile != uniqueId) {
            fprintf(tempFilePointer, "%d %d %s\n", uniqueIdFromFile, port, ipOfClients);
        }
    }
    fclose(filePointer);
    fclose(tempFilePointer);
    remove(CLIENT_DETAILS_FILE);
    rename("temp.log", CLIENT_DETAILS_FILE);
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

// Function to handle each client connection
void receivePingFromClient(int clientSocket) {
    int receiveStatus;
    struct sockaddr_in clientAddress;
    socklen_t addressSize = sizeof(clientAddress);
    char buffer[MESSAGE_SIZE];

    while (1) {
        bzero(buffer, MESSAGE_SIZE);
        receiveStatus = recv(clientSocket, buffer, sizeof(buffer), 0);

        if (receiveStatus <= 0) {
            continue;
        }

        // If logout string is received, close the connection
        if (strcmp(buffer, "logout") == 0) {
            printf("Client disconnected.\n");
            sendAcknowledgementToClient(clientSocket, ACK_CLOSE_MESSAGE);
            break;
        }
        // If message is 'active', then send the active list of clients
        else if (strcmp(buffer, "active") == 0) {
            ClientDetails *clientDetails = readClientDetailsFromFile();
            char activeClients[MESSAGE_SIZE];
            bzero(activeClients, MESSAGE_SIZE);
            for (int i = 0; i < clientDetails->count; i++) {
                char temp[MESSAGE_SIZE];
                if (clientDetails->clientDetail[i].uniqueId == clientUniqueId) {
                    sprintf(temp, "%d\t%d\t(You)\n", clientDetails->clientDetail[i].uniqueId, clientDetails->clientDetail[i].port);
                } else {
                    sprintf(temp, "%d\t%d\n", clientDetails->clientDetail[i].uniqueId, clientDetails->clientDetail[i].port);
                }
                strcat(activeClients, temp);
            }
            sendAcknowledgementToClient(clientSocket, activeClients);
        }
        // If message is 'sent', then message format send <dest_id> <message>. Use the dest_id to send the message to the client
        else if (strncmp(buffer, "send", 4) == 0) {
            char *token = strtok(buffer, " ");
            token = strtok(NULL, " ");
            int destId = atoi(token);

            // The remaining part of buffer is the message. Now do not consider space as seperator.
            token = strtok(NULL, "");
            char message[MESSAGE_SIZE];
            bzero(message, MESSAGE_SIZE);
            strcpy(message, token);

            // adding 0 at the end of message. Also adding a comment 'sent from client<clientnumber>'
            int i;
            for (i = 0; i < strlen(message); i++) {
                if (message[i] == '\n') {
                    message[i] = '\0';
                    break;
                }
            }
            strcat(message, " sent from client");
            char temp[10];
            sprintf(temp, "%d", clientUniqueId);
            strcat(message, temp);
            printf("Message to be sent: %s\n", message);

            // Check if the client is active
            int clientFound = 0;
            ClientDetails *clientDetails = readClientDetailsFromFile();
            for (int i = 0; i < clientDetails->count; i++) {
                if (clientDetails->clientDetail[i].uniqueId == destId) {
                    clientFound = 1;
                    break;
                }
            }

            if (clientFound == 0) {
                sendAcknowledgementToClient(clientSocket, ACK_ERROR_CLIENT_NOT_FOUND);
            } else {
                // Send the message to the client
                int destPort;
                char destIp[100];
                for (int i = 0; i < clientDetails->count; i++) {
                    if (clientDetails->clientDetail[i].uniqueId == destId) {
                        destPort = clientDetails->clientDetail[i].port;
                        strcpy(destIp, clientDetails->clientDetail[i].ip);
                        break;
                    }
                }

                int destSocket = socket(AF_INET, SOCK_STREAM, 0);
                if (destSocket < 0) {
                    perror("Error in creating socket");
                    exit(1);
                }

                struct sockaddr_in destAddress;
                memset(&destAddress, '\0', sizeof(destAddress));
                destAddress.sin_family = AF_INET;
                destAddress.sin_port = htons(destPort);
                destAddress.sin_addr.s_addr = inet_addr(destIp);

                if (connect(destSocket, (struct sockaddr *)&destAddress, sizeof(destAddress)) < 0) {
                    perror("Error in connecting to client");
                    exit(1);
                }

                send(destSocket, message, strlen(message), 0);
                close(destSocket);
                sendAcknowledgementToClient(clientSocket, ACK_MESSAGE_SEND_TO_CLIENT);
            }
        }
        else{
            printf("Message from client: %s\n", buffer);
            sendAcknowledgementToClient(clientSocket, buffer);
        }

    }

    close(clientSocket);
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

// Function to accept incoming connections and create a thread for each connection
void acceptIncomingConnectionsAndCreateThread(int serverSocket) {
    int clientSocket;
    struct sockaddr_in clientAddress;
    socklen_t addressSize = sizeof(clientAddress);

    pid_t childpid;

    char buffer[1024];

    while (1) {
        // Accepting incoming connections
        clientSocket = accept(serverSocket, (struct sockaddr *)&clientAddress, &addressSize);
        if (clientSocket < 0) {
            perror("Error. Could not accept connection");
            exit(1);
        }
        printf("Client connected.\n");

        printf("Connection accepted from %s:%d\n", inet_ntoa(clientAddress.sin_addr), ntohs(clientAddress.sin_port));

        // store the client details in the file
        clientUniqueId = clientAddress.sin_port;
        storeClientDetailsInFile(clientUniqueId, ntohs(clientAddress.sin_port), clientAddress);

        if((childpid = fork()) == 0){
			//close(serverSocket);

			receivePingFromClient(clientSocket);

            // remove the client details from the file
            removeClientDetailsFromFile(clientUniqueId);

            // close the client socket
            close(clientSocket);
		}

        // Creating a child process for each connection


    //     int *newClientSocket = malloc(1);
    //     *newClientSocket = clientSocket;

    //     if (pthread_create(&thread_id, NULL, receivePingFromClient, (void *)newClientSocket) != 0) {
    //         perror("Error. Could not create thread");
    //         exit(1);
    //     }
    //     pthread_detach(thread_id);
    }

    // pthread_exit(NULL);
}

void main(int argc, char *argv[]) {

    int serverSocket, port;
    struct sockaddr_in serverAddress;

    // Clear the file
    clearFile(CLIENT_DETAILS_FILE);

    // Reading port from command line arguments
    if (argc != 3) {
        printf("Usage: %s <server_ip> <port>\n", argv[0]);
        exit(1);
    }
    
    char *ipOfServer = argv[1];
    port = atoi(argv[2]);

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
