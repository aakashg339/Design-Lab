#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>

#define MESSAGE_SIZE 1024

#define MESSAGE_END_TRANSFER "MESSAGE_END_TRANSFER"

#define ACK_MESSAGE "SUCCESS"
#define ACK_CLOSE_MESSAGE "ACK_CLOSE"
#define ACK_FILE_ERROR_MESSAGE "ACK_FILE_ERROR"
#define ACK_DIRECTORY_ERROR_MESSAGE "ACK_DIRECTORY_ERROR"
#define ACK_TRANSFER_BEGIN_MESSAGE "ACK_TRANSFER_BEGIN"
#define ACK_LS_ERROR_MESSAGE "ACK_LS_ERROR"

pthread_mutex_t mutex;

// Function to create TCP socket
int createSocket() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("Error creating socket.");
        exit(1);
    }
    printf("TCP server socket created.\n");
    return sock;
}

// Function to assign address to socket
void assignAddressToSocket(int sock, struct sockaddr_in *address, char *ipOfServer, int portOfServer) {
    memset(address, '\0', sizeof(*address));
    address->sin_family = AF_INET;
    address->sin_port = htons(portOfServer);
    address->sin_addr.s_addr = inet_addr(ipOfServer);
}

// Function to connect to the server
void connectToServer(int sock, struct sockaddr_in *address) {
    if (connect(sock, (struct sockaddr*)address, sizeof(*address)) < 0) {
        perror("Not able to connect to server.");
        exit(1);
    }
    printf("Connected to the server.\n");
}

// Function to close the socket
void closeSocket(int sock) {
    close(sock);
    printf("Socket closed from client side.\n");
}

// Function to send acknowledgement to the client
void sendAcknowledgementToServer(int serverSocket, char *ackMessage) {
    char buffer[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    strcpy(buffer, ackMessage);
    send(serverSocket, buffer, strlen(buffer), 0);
}

// Function to read the command from the terminal and send to the server
void pingTheServer(int sock) {
    char buffer[MESSAGE_SIZE];

    while(1) {
        bzero(buffer, MESSAGE_SIZE);
        fgets(buffer, MESSAGE_SIZE, stdin);

        // Remove trailing newline character
        buffer[strcspn(buffer, "\n")] = 0;

        // Check the message to be sent
        if(strcmp(buffer, "/logout") == 0) {
            send(sock, buffer, strlen(buffer), 0);
            break;
        }
        else {
            send(sock, buffer, strlen(buffer), 0);
        }
    }
}

void* captureResponseAndPrint(void *args) {
    char buffer[MESSAGE_SIZE];
    ssize_t receiveStatus;
    int sock = *(int *)args;

    while(1) {
        bzero(buffer, MESSAGE_SIZE);
        receiveStatus = recv(sock, buffer, sizeof(buffer), 0);

        if(receiveStatus > 0) {
            buffer[receiveStatus] = '\0';
            printf("%s\n", buffer);
        }

        if(receiveStatus <= 0) {
            continue;
        }
    }
}

// Function to start listening to the server
void startListeningToServer(int sock) {
    pthread_t thread;
    int *serverSocket = (int *)malloc(sizeof(int));
    *serverSocket = sock;
    
    if(pthread_create(&thread, NULL, captureResponseAndPrint, (void *)serverSocket) < 0) {
        perror("Error creating thread.");
        exit(1);
    }
}

void main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <server_ip> <port>\n", argv[0]);
        exit(1);
    }

    char *ipOfServer = argv[1];
    int serverPort = atoi(argv[2]);
    int socketC;
    struct sockaddr_in address;

    // initialize mutex
    pthread_mutex_init(&mutex, NULL);

    // Create TCP socket
    socketC = createSocket();

    // Assign address to socket
    assignAddressToSocket(socketC, &address, ipOfServer, serverPort);

    // Connect to the server
    connectToServer(socketC, &address);

    // start thread for listening to the server
    startListeningToServer(socketC);

    // Send ping requests to the server
    pingTheServer(socketC);

    // Close the socket
    closeSocket(socketC);

    // destroy mutex
    pthread_mutex_destroy(&mutex);
}
