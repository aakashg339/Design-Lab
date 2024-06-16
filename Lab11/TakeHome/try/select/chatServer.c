#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define MESSAGE_SIZE 1024

#define MAX_QA 250

#define SERVER_BACKLOG 10

#define CHAT_HISTORY_SIZE 100

#define ACK_INVALID_COMMAND "Invalid command."
#define ACK_INVALID_DESTINATION_ID "Invalid destination ID."
#define ACK_MAXIMUM_CLIENT_LIMIT_REACHED "Maximum client limit reached."

#define CHATBOT_INVALID_COMMAND_MESSAGE "System Malfunction, I couldnot understand your query."
#define CHATBOT_LOGIN_MESSAGE "Hi, I am stupid bot, I am able to answer a limited set of your questions"
#define CHATBOT_LOGOUT_MESSAGE "Bye, Have a nice day and do not complain about me"

// Structure to store the client details
typedef struct clientDetail {
    int id;
    int socketFD;
    int isChatting;
} clientDetail;

// clientDetails list to store details of n clients
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

// Structure to store chat history for each client
typedef struct chatHistory {
    int clientId;
    char *chat;
} chatHistory;

// Structure to store maximum n chat histories for each client
typedef struct chatHistories {
    chatHistory *ch[CHAT_HISTORY_SIZE];
    int size;
    int isValid;
} chatHistories;

// chatHistory list to store chat history of n clients
chatHistories *chatHistoriesList[SERVER_BACKLOG];

// Function to initialize the client details
void initializeClientDetailsAndChatBot() {
    int i, j;

    // Initializing the client details
    for (i = 0; i < SERVER_BACKLOG; i++) {
        clientDetails[i] = (clientDetail *)malloc(sizeof(clientDetail));
        clientDetails[i]->id = -1;
        clientDetails[i]->socketFD = -1;
        clientDetails[i]->isChatting = 0;
    }
    clientCount = 0;

    // Initializing the chatbot
    cb = (chatbot *)malloc(sizeof(chatbot));
    for (i = 0; i < MAX_QA; i++) {
        cb->qa[i] = (questionAndAnswer *)malloc(sizeof(questionAndAnswer));
        cb->qa[i]->question = (char *)malloc(MESSAGE_SIZE);
        cb->qa[i]->answer = (char *)malloc(MESSAGE_SIZE);
    }

    cb->size = 0;

    // Initializing the chat histories
    for (i = 0; i < SERVER_BACKLOG; i++) {
        chatHistoriesList[i] = (chatHistories *)malloc(sizeof(chatHistories));
        for (j = 0; j < CHAT_HISTORY_SIZE; j++) {
            chatHistoriesList[i]->ch[j] = (chatHistory *)malloc(sizeof(chatHistory));
            chatHistoriesList[i]->ch[j]->chat = (char *)malloc(MESSAGE_SIZE);
        }
        chatHistoriesList[i]->size = 0;
        chatHistoriesList[i]->isValid = 0;
    }

    printf("Client details initialized.\n");
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

// Function to convert the string to lower case
char* convertStringToLower (char* s) {
    for (int i = 0; i < strlen(s); ++i)
        if (s[i] >= 'A' && s[i] <= 'Z')
            s[i] += 'a' - 'A';
    return s;
}

// Function to store the client details
int storeClientDetails(int id, int socket) {
    int i;
    for (i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->id == -1) {
            clientDetails[i]->id = id;
            clientDetails[i]->socketFD = socket;
            clientCount++;
            break;
        }
    }
    if (i == SERVER_BACKLOG) {
        return -1;
    }
    printf("Client %d details stored.\n", id);
    return 0;
}

// Function to remove the client details
void removeClientDetails(int id) {
    for (int i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->id == id) {
            clientDetails[i]->id = -1;
            clientDetails[i]->socketFD = -1;
            clientDetails[i]->isChatting = 0;
            clientCount--;
            break;
        }
    }
    printf("Client %d details removed.\n", id);
}

// Function to get client ids as a string
char *getClientIds(int clientOwnSocket) {
    char buffer[MESSAGE_SIZE];
    char temp[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    bzero(temp, MESSAGE_SIZE);

    for (int i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->id != -1) {
            bzero(temp, MESSAGE_SIZE);
            if(clientDetails[i]->socketFD == clientOwnSocket) {
                sprintf(temp, "%d (Own)\n", clientDetails[i]->id);
            }
            else {
                sprintf(temp, "%d\n", clientDetails[i]->id);
            
            }
            strcat(buffer, temp);
        }
    }
    
    return strdup(buffer);
}

int getClientId(int clientSocket) {
    for (int i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->socketFD == clientSocket) {
            return clientDetails[i]->id;
        }
    }
    return -1;
}

// Function to set the chatbot status
void setChatBotStatusOfClient(int clientSocket, int status) {
    int i, clientId;
    for (i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->socketFD == clientSocket) {
            clientDetails[i]->isChatting = status;
            clientId = clientDetails[i]->id;
            break;
        }
    }

    printf("Client %d chatbot status set to %d.\n", clientId, status);
}

// Function to get the chatbot status
int getChatBotStatusOfClient(int clientSocket) {
    int i;
    for (i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->socketFD == clientSocket) {
            return clientDetails[i]->isChatting;
        }
    }
    return -1;
}

// Function to store the chat history
void storeChatHistory(int clientId, char *chat) {
    int i, j;
    for (i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->id == clientId) {
            for (j = 0; j < CHAT_HISTORY_SIZE; j++) {
                if (chatHistoriesList[i]->ch[j]->clientId == -1) {
                    chatHistoriesList[i]->ch[j]->clientId = clientId;
                    strcpy(chatHistoriesList[i]->ch[j]->chat, chat);
                    chatHistoriesList[i]->size++;
                    break;
                }
            }
            break;
        }
    }
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

        // Remove leading and trailing spaces
        question = trimString(question);
        answer = trimString(answer);

        // converting the question to lower case
        question = convertStringToLower(question);

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

    fclose(file);

    printf("Chatbot data loaded.\n");
}

// Function to send acknowledgement to the client
void sendAcknowledgementToClient(int clientSocket, char *ackMessage) {
    char buffer[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    strcpy(buffer, ackMessage);
    printf("Sending acknowledgement to client: %s\n", buffer);
    send(clientSocket, buffer, strlen(buffer), 0);
}

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }
    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

// Function to generate random uid of 4 digits such that it is not already assigned
int generateUid() {
    int uid = -1;
    while (1) {
        uid = rand() % 9000 + 1000;
        int flag = 0;
        for (int i = 0; i < SERVER_BACKLOG; i++) {
            if (clientDetails[i]->id == uid) {
                flag = 1;
                break;
            }
        }
        if (flag == 0) {
            break;
        }
    }
    return uid;
}

// Function to keep track of the client details
int assignUidAndStoreClientDetails(int clientSocket) {
    int uid = generateUid();
    return storeClientDetails(uid, clientSocket);
}

// Function to handle the chatbot
void chatbotHandler(char *request, int clientSocket) {
    char *question = trimString(request);
    char *answer = NULL;
    int flag = 0;

    // If /chatbot logout is entered, then set the chatbot status to 0
    if (strcmp(question, "/chatbot logout") == 0) {
        setChatBotStatusOfClient(clientSocket, 0);
        sendAcknowledgementToClient(clientSocket, CHATBOT_LOGOUT_MESSAGE);
        return;
    }

    for (int i = 0; i < cb->size; i++) {
        if (strcmp(cb->qa[i]->question, question) == 0) {
            answer = cb->qa[i]->answer;
            flag = 1;
            break;
        }
    }

    if (flag == 0) {
        sendAcknowledgementToClient(clientSocket, CHATBOT_INVALID_COMMAND_MESSAGE);
    } else {
        sendAcknowledgementToClient(clientSocket, answer);
    }
}

// Function to handle the client request
int handleClientRequest(int clientSocket, char *request) {
    // Implement the following features for the clients:-
    // i. “/active” - retrieve a list of active clients
    // ii. "/send <dest_id> <message>" - send messages to other clients using their
    // unique IDs
    // iii. “/logout” - client requests to exit the application. In such cases also, the
    // server must send a message “Bye!! Have a nice day” as an acknowledgement
    // to the client.
    int chatbotStatus = getChatBotStatusOfClient(clientSocket);

    // remove leading and trailing spaces and convert to lowercase
    request = trimString(request);
    request = convertStringToLower(request);

    if (chatbotStatus == 1) {
        chatbotHandler(request, clientSocket);
        return 0;
    }

    // printf("Request : %s\n", request);

    char *command = strtok(request, " ");
    // printf("Command : %s\n", command);
    if (command == NULL) {
        sendAcknowledgementToClient(clientSocket, "Invalid command.");
        return 0;
    }

    if (strcmp(command, "/active") == 0) {
        char *clientIds = getClientIds(clientSocket);
        sendAcknowledgementToClient(clientSocket, clientIds);
        free(clientIds);
    } else if (strcmp(command, "/send") == 0) {
        char *destId = strtok(NULL, " ");
        char *message = strtok(NULL, "\0");

        // getting source id
        int sourceId = getClientId(clientSocket);

        if (destId == NULL || message == NULL) {
            sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND);
            return 0;
        }

        int destSocket = -1;
        for (int i = 0; i < SERVER_BACKLOG; i++) {
            if (clientDetails[i]->id == atoi(destId)) {
                destSocket = clientDetails[i]->socketFD;
                break;
            }
        }

        if (destSocket == -1) {
            sendAcknowledgementToClient(clientSocket, ACK_INVALID_DESTINATION_ID);
            return 0;
        }

        char buffer[MESSAGE_SIZE];
        bzero(buffer, MESSAGE_SIZE);
        sprintf(buffer, "Message from %d: %s", sourceId, message);
        send(destSocket, buffer, strlen(buffer), 0);
    } else if (strcmp(command, "/logout") == 0) {
        sendAcknowledgementToClient(clientSocket, "Bye!! Have a nice day");
        return -1;
    } else if (strcmp(command, "/chatbot") == 0) {
        char *subCommand = strtok(NULL, "");
        if (strcmp(subCommand, "login") == 0) {
            setChatBotStatusOfClient(clientSocket, 1);
            sendAcknowledgementToClient(clientSocket, CHATBOT_LOGIN_MESSAGE);
        } else if (strcmp(subCommand, "logout") == 0) {
            setChatBotStatusOfClient(clientSocket, 0);
            sendAcknowledgementToClient(clientSocket, CHATBOT_LOGOUT_MESSAGE);
        } else {
            sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND);
        }
        return 0;
    } else {
        sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND);
    }

    return 0;
}

void main(int argc, char *argv[]) {
    // Loading the chatbot data
    initializeClientDetailsAndChatBot();
    loadChatbot();

    int clientId = -1;

    // Reading port from command line arguments
    if (argc != 2) {
        printf("Usage: %s <port>\n", argv[0]);
        exit(1);
    }
    
    char *port = argv[1];

    fd_set master; // master file descriptor list
    fd_set read_fds; // temp file descriptor list for select()
    int fdmax; // maximum file descriptor number

    int listener; // listening socket descriptor
    int newfd; // newly accept()ed socket descriptor
    struct sockaddr_storage remoteaddr; // client address
    socklen_t addrlen;

    char buf[MESSAGE_SIZE]; // buffer for client data
    int nbytes;
    int status;

    char remoteIP[INET6_ADDRSTRLEN];

    int yes = 1; // for setsockopt() SO_REUSEADDR, below
    int i, j, rv;

    struct addrinfo hints, *ai, *p;

    FD_ZERO(&master); // clear the master and temp sets
    FD_ZERO(&read_fds);

    // get us a socket and bind it
    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE;

    if ((rv = getaddrinfo(NULL, port, &hints, &ai)) != 0) {
        fprintf(stderr, "selectserver: %s\n", gai_strerror(rv));
        exit(1);
    }

    for (p = ai; p != NULL; p = p->ai_next) {
        listener = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if (listener < 0) {
            continue;
        }

        // lose the pesky "address already in use" error message
        setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));

        if (bind(listener, p->ai_addr, p->ai_addrlen) < 0) {
            close(listener);
            continue;
        }

        break;
    }

    // if we got here, it means we didn't get bound
    if (p == NULL) {
        fprintf(stderr, "selectserver: failed to bind\n");
        exit(2);
    }

    freeaddrinfo(ai); // all done with this

    // listen
    if (listen(listener, SERVER_BACKLOG) == -1) {
        perror("listen");
        exit(3);
    }

    printf("Server started on port %s\n", port);

    // add the listener to the master set
    FD_SET(listener, &master);

    // keep track of the biggest file descriptor
    fdmax = listener; // so far, it's this one

    // main loop
    for (;;) {
        read_fds = master; // copy it
        if (select(fdmax + 1, &read_fds, NULL, NULL, NULL) == -1) {
            perror("select");
            exit(4);
        }

        // run through the existing connections looking for data to read
        for (i = 0; i <= fdmax; i++) {
            if (FD_ISSET(i, &read_fds)) { // we got one!!
                if (i == listener) {
                    // handle new connections
                    addrlen = sizeof remoteaddr;
                    newfd = accept(listener, (struct sockaddr *)&remoteaddr, &addrlen);

                    if (newfd == -1) {
                        perror("accept");
                    } else {
                        status = assignUidAndStoreClientDetails(newfd);
                        if (status == -1) {
                            perror("Maximum. client limit reached");
                            sendAcknowledgementToClient(newfd, ACK_MAXIMUM_CLIENT_LIMIT_REACHED);
                            close(newfd);
                            continue;
                        }
                        FD_SET(newfd, &master); // add to master set
                        if (newfd > fdmax) { // keep track of the max
                            fdmax = newfd;
                        }
                        printf("selectserver: new connection from %s on socket %d\n", inet_ntop(remoteaddr.ss_family, get_in_addr((struct sockaddr *)&remoteaddr), remoteIP, INET6_ADDRSTRLEN), newfd);
                    }
                } else {
                    clientId = getClientId(i);
                    // handle data from a client
                    bzero(buf, MESSAGE_SIZE);
                    if ((nbytes = recv(i, buf, sizeof buf, 0)) <= 0) {
                        // got error or connection closed by client
                        if (nbytes == 0) {
                            // connection closed
                            printf("selectserver: socket %d hung up\n", clientId);
                        } else {
                            perror("recv");
                        }
                        close(i); // bye!
                        FD_CLR(i, &master); // remove from master set
                        removeClientDetails(clientId);
                    } else {
                        // we got some data from a client
                        status = handleClientRequest(i, buf);
                        if (status == -1) {
                            close(i); // bye!
                            FD_CLR(i, &master); // remove from master set
                            removeClientDetails(clientId);
                        }
                    } // END handle data from client
                } // END handle data from client
            } // END got new incoming connection
        } // END looping through file descriptors
    } // END for(;;)--and you thought it would never end!
}