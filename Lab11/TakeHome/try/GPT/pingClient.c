#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <signal.h>

#define MESSAGE_SIZE 2048

int socketC;

// Function to send a message to the server
void sendMessageToServer(int serverSocket, const char *message) {
    char buffer[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    strncpy(buffer, message, MESSAGE_SIZE);
    send(serverSocket, buffer, strlen(buffer), 0);
}

// Signal handler for graceful shutdown on Ctrl+C or Ctrl+Z
void signalHandler(int sig) {
    if (sig == SIGINT || sig == SIGTSTP) {
        printf("\nDetected signal %d. Exiting gracefully.\n", sig);
        sendMessageToServer(socketC, "\\logout");
        close(socketC);
        exit(0);
    }
}

// Create and connect the socket to server
void setupConnection(char *ipOfServer, int portOfServer) {
    struct sockaddr_in address;
    
    // Creating socket
    socketC = socket(AF_INET, SOCK_STREAM, 0);
    if (socketC == -1) {
        perror("Failed to create socket");
        exit(EXIT_FAILURE);
    }
    printf("TCP socket created.\n");

    // Configuring server address structure
    address.sin_family = AF_INET;
    address.sin_port = htons(portOfServer);
    if (inet_pton(AF_INET, ipOfServer, &address.sin_addr) <= 0) {
        printf("Invalid address/ Address not supported.\n");
        exit(EXIT_FAILURE);
    }

    // Connecting to the server
    if (connect(socketC, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Connection Failed");
        exit(EXIT_FAILURE);
    }
    printf("Connected to the server.\n");
}

void interactWithServer() {
    char buffer[MESSAGE_SIZE];
    
    while (1) {
        printf("Client> ");
        fgets(buffer, MESSAGE_SIZE, stdin);
        buffer[strcspn(buffer, "\n")] = 0; // Removing newline char

        sendMessageToServer(socketC, buffer);

        if (strcmp(buffer, "\\logout") == 0) {
            printf("Logging out...\n");
            
            // Wait for logout confirmation from server
            bzero(buffer, MESSAGE_SIZE);
            recv(socketC, buffer, MESSAGE_SIZE, 0);
            printf("Server: %s\n", buffer);
            
            if (strcmp(buffer, "ACK_LOGOUT") == 0) {
                break; // Exit loop on successful logout acknowledgment
            } else {
                printf("Error logging out. Server response: %s\n", buffer);
                // Handle error or unexpected server response here
            }
        } else {
            bzero(buffer, MESSAGE_SIZE);
            recv(socketC, buffer, MESSAGE_SIZE, 0);
            printf("Server: %s\n", buffer);
        }
    }
}


int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <IP of Server> <Port>\n", argv[0]);
        return 1;
    }

    char *serverIP = argv[1];
    int serverPort = atoi(argv[2]);

    // Setting up signal handling for graceful shutdown
    signal(SIGINT, signalHandler);
    signal(SIGTSTP, signalHandler);

    setupConnection(serverIP, serverPort);
    interactWithServer();

    close(socketC);
    return 0;
}
