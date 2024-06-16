#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <signal.h>

#define MESSAGE_SIZE 2048

#define MESSAGE_END_TRANSFER "MESSAGE_END_TRANSFER"

#define ACK_MESSAGE "SUCCESS"
#define ACK_CLOSE_MESSAGE "ACK_CLOSE"
#define ACK_FILE_ERROR_MESSAGE "ACK_FILE_ERROR"
#define ACK_DIRECTORY_ERROR_MESSAGE "ACK_DIRECTORY_ERROR"
#define ACK_TRANSFER_BEGIN_MESSAGE "ACK_TRANSFER_BEGIN"
#define ACK_LS_ERROR_MESSAGE "ACK_LS_ERROR"

int socketC;

// Function to send acknowledgement to the client
void sendAcknowledgementToServer(int serverSocket, char *ackMessage) {
    char buffer[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    strcpy(buffer, ackMessage);
    send(serverSocket, buffer, strlen(buffer), 0);
}

void sendCloseMessageToServer(int serverSocket) {
    sendAcknowledgementToServer(serverSocket, "logout");
}

// Function to handle the signal ctrl+c. On ctrl+c, send \logout to the server to close the connection
void signalHandlerForCtrlC(int sig) {
    if (sig == SIGINT) {
        printf("Ctrl+C pressed. Exiting.\n");
        sendCloseMessageToServer(socketC);
    }
}

// Function to handle the signal ctrl+z. On ctrl+z, send \logout to the server to close the connection
void signalHandlerForCtrlZ(int sig) {
    if (sig == SIGTSTP) {
        printf("Ctrl+Z pressed. Exiting.\n");
        sendCloseMessageToServer(socketC);
    }
}

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
void assignAddressToSocket(struct sockaddr_in *address, char *ipOfServer, int portOfServer) {
    memset(address, '\0', sizeof(*address));
    address->sin_family = AF_INET;
    address->sin_port = htons(portOfServer);
    address->sin_addr.s_addr = inet_addr(ipOfServer);
}

// Function to connect to the server
void connectToServer(struct sockaddr_in *address) {
    if (connect(socketC, (struct sockaddr*)address, sizeof(*address)) < 0) {
        perror("Not able to connect to server.");
        exit(1);
    }
    printf("Connected to the server.\n");
}

// Function to close the socket
void closeSocket() {
    close(socketC);
    printf("Socket closed from client side.\n");
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

// Function to chat with the chatbot
void chatbotFeature() {
    char buffer[MESSAGE_SIZE];
    int n;
    int isError = 0;
        while (1)
        {
            // get the response from the server
            bzero(buffer, MESSAGE_SIZE);
            n = read(socketC, buffer, sizeof(buffer));
            if (n < 0)
            {
                perror("Error in reading from server.");
                exit(1);
            }

            printf("stupidbot> %s\n", buffer);

            if (strcmp(buffer, "Bye! Have a nice day and do not complain about me") == 0)
            {
                break;
            }

            bzero(buffer, MESSAGE_SIZE);
            printf("user> ");
            fgets(buffer, MESSAGE_SIZE, stdin);
            buffer[strcspn(buffer, "\n")] = 0;
            isError = send(socketC, buffer, strlen(buffer), 0);

            if (isError < 0)
            {
                perror("Error in sending message to server.");
                exit(1);
            }
        }
}

// Function to read the command from the terminal and send to the server
void pingTheServer() {
    char buffer[MESSAGE_SIZE];
    int n;

    int pid;

    if ((pid = fork()) == 0)
    {
        int isError = 0;
        while (1)
        {
            bzero(buffer, MESSAGE_SIZE);
            fgets(buffer, MESSAGE_SIZE, stdin);
            buffer[strcspn(buffer, "\n")] = 0;
            isError = send(socketC, buffer, strlen(buffer), 0);
            if (isError < 0)
            {
                perror("Error in sending message to server.");
                exit(1);
            }

            if (strncmp(buffer, "logout", 7) == 0)
            {
                printf("Disconnected from server.\n");
                close(socketC);
                exit(0);
            }
            else if (strcmp(buffer, "chatbot login") == 0) {
                // send the message to server
                sendAcknowledgementToServer(socketC, buffer);
                chatbotFeature();
            }
        }
    }
    else
    {
        bzero(buffer, MESSAGE_SIZE);
        while ((n = read(socketC, buffer, sizeof(buffer))) != 0)
        {
            if (n < 0)
            {
                perror("Error in reading from server.");
                exit(1);
            }

            if (strncmp(buffer, ACK_CLOSE_MESSAGE, strlen(ACK_CLOSE_MESSAGE)) == 0)
            {
                close(socketC);
                exit(0);
            }

            printf("%s\n", buffer);
            bzero(buffer, MESSAGE_SIZE);
        }
    }
}

void main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <server_ip> <port>\n", argv[0]);
        exit(1);
    }

    char *ipOfServer = argv[1];
    int serverPort = atoi(argv[2]);
    struct sockaddr_in address;

    // Set the signal handler
    signal(SIGINT, signalHandlerForCtrlC);
    signal(SIGTSTP, signalHandlerForCtrlZ);

    // Create TCP socket
    socketC = createSocket();

    // Assign address to socket
    assignAddressToSocket(&address, ipOfServer, serverPort);

    // Connect to the server
    connectToServer(&address);

    // Send ping requests to the server
    pingTheServer();

    // Close the socket
    closeSocket();

}
