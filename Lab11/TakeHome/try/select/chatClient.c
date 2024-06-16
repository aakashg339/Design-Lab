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
#define ACK_MAXIMUM_CLIENT_LIMIT_REACHED "Maximum client limit reached."

#define CHATBOT_LOGOUT_MESSAGE "Bye, Have a nice day and do not complain about me"

int isChatbotOn = 0;
int isServerLimitReached = 0;

pthread_mutex_t mutex;

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

// switch on the chatbot
void switchOnChatbot() {
    pthread_mutex_lock(&mutex);
    isChatbotOn = 1;
    pthread_mutex_unlock(&mutex);
}

// switch off the chatbot
void switchOffChatbot() {
    pthread_mutex_lock(&mutex);
    isChatbotOn = 0;
    pthread_mutex_unlock(&mutex);
}

int getChatbotStatus() {
    int status;
    pthread_mutex_lock(&mutex);
    status = isChatbotOn;
    pthread_mutex_unlock(&mutex);
    return status;
}

void setServerLimitReached() {
    pthread_mutex_lock(&mutex);
    isServerLimitReached = 1;
    pthread_mutex_unlock(&mutex);
}

int getServerLimitReached() {
    int status;
    pthread_mutex_lock(&mutex);
    status = isServerLimitReached;
    pthread_mutex_unlock(&mutex);
    return status;
}

// Function to read the command from the terminal and send to the server
void pingTheServer(int sock) {
    
    char buffer[MESSAGE_SIZE];
    int chatbotStatus;

    while(1) {
        bzero(buffer, MESSAGE_SIZE);
        sleep(1);

        if(getServerLimitReached() == 1) {
            break;
        }

        chatbotStatus = getChatbotStatus();
        if(chatbotStatus == 1) {
            printf("user>:");
        }
        fgets(buffer, MESSAGE_SIZE, stdin);

        // Remove trailing newline character
        buffer[strcspn(buffer, "\n")] = 0;

        // remove leading and trailing spaces
        char *message = trimString(buffer);
        // printf("Message: %s\n", message);

        // Check the message to be sent
        if(strcmp(message, "/logout") == 0) {
            send(sock, message, strlen(message), 0);
            break;
        }
        else if(strcmp(message, "/chatbot login") == 0) {
            switchOnChatbot();
        }
        
        send(sock, message, strlen(message), 0);
    }
}

void* captureResponseAndPrint(void *args) {
    char buffer[MESSAGE_SIZE];
    ssize_t receiveStatus;
    int sock = *(int *)args;
    int chatBotStatus;

    while(1) {
        bzero(buffer, MESSAGE_SIZE);
        receiveStatus = recv(sock, buffer, sizeof(buffer), 0);

        if(receiveStatus > 0) {
            buffer[receiveStatus] = '\0';

            if(strcmp(buffer, ACK_MAXIMUM_CLIENT_LIMIT_REACHED) == 0) {
                setServerLimitReached();
                printf("%s\n", buffer);
                break;
            }

            chatBotStatus = getChatbotStatus();
            if(chatBotStatus == 1) {
                printf("stupidbot>: %s\n", buffer);
                if(strcmp(buffer, CHATBOT_LOGOUT_MESSAGE) == 0) {
                    switchOffChatbot();
                }
            }
            else {
                printf("%s\n", buffer);
            }
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

    // set isChatbotOn to 0. 0 means chatbot is off and 1 means chatbot is on
    isChatbotOn = 0;

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
