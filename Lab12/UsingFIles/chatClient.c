#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/signal.h>

#define MESSAGE_SIZE 2048

#define MESSAGE_END_TRANSFER "MESSAGE_END_TRANSFER"

#define ACK_MESSAGE "SUCCESS"
#define ACK_CLOSE_MESSAGE "ACK_CLOSE"
#define ACK_FILE_ERROR_MESSAGE "ACK_FILE_ERROR"
#define ACK_DIRECTORY_ERROR_MESSAGE "ACK_DIRECTORY_ERROR"
#define ACK_TRANSFER_BEGIN_MESSAGE "ACK_TRANSFER_BEGIN"
#define ACK_LS_ERROR_MESSAGE "ACK_LS_ERROR"
#define ACK_MAXIMUM_CLIENT_LIMIT_REACHED "Maximum client limit reached."
#define ACK_LOGOUT_MESSAGE "Bye!! Have a nice day"

#define CHATBOT_LOGOUT_MESSAGE "Bye, Have a nice day and do not complain about me"

#define CHATBOT_V2_LOGOUT_MESSAGE "Bye! Have a nice day and hope you do not have any complaints about me"

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

// Function to handle recv and send messages as parent and child process. 
void pingTheServer(int sock) {
    int chatbotStatus;

    pid_t pid;

    if((pid = fork()) == 0) {
        chatbotStatus = 0;
        while(1) {
            char buffer[MESSAGE_SIZE];
            bzero(buffer, MESSAGE_SIZE);
            sleep(1);
            if (chatbotStatus == 1 ) {
                printf("user> ");
            }
            else if (chatbotStatus == 2) {
                sleep(4);
                printf("user> ");
            }
            fgets(buffer, MESSAGE_SIZE, stdin);

            // Remove trailing newline character
            buffer[strcspn(buffer, "\n")] = 0;
            
            // remove leading and trailing spaces
            char *trimmedBuffer = trimString(buffer);
            strcpy(buffer, trimmedBuffer);


            if (strlen(buffer) == 0) {
                continue;
            }

            if (strcmp(buffer, "/chatbot login") == 0) {
                chatbotStatus = 1;
            }
            else if (strcmp(buffer, "/chatbot logout") == 0) {
                chatbotStatus = 0;
            }
            else if (strcmp(buffer, "/chatbot_v2 login") == 0) {
                chatbotStatus = 2;
            }
            else if (strcmp(buffer, "/chatbot_v2 logout") == 0) {
                chatbotStatus = 0;
            }
            

            send(sock, buffer, strlen(buffer), 0);
        }
    } else {
        while(1) {
            char buffer[MESSAGE_SIZE];
            bzero(buffer, MESSAGE_SIZE);
            recv(sock, buffer, MESSAGE_SIZE, 0);
            if (strcmp(buffer, ACK_LOGOUT_MESSAGE) == 0) {
                // Kill the child process
                printf("%s\n", buffer);
                kill(pid, SIGKILL);
                break;
            }
            printf("%s\n", buffer);
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
    int socketC;
    struct sockaddr_in address;

    // Create TCP socket
    socketC = createSocket();

    // Assign address to socket
    assignAddressToSocket(socketC, &address, ipOfServer, serverPort);

    // Connect to the server
    connectToServer(socketC, &address);

    // Send ping requests to the server
    pingTheServer(socketC);

    // Close the socket
    closeSocket(socketC);
}
