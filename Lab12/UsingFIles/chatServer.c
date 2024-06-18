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
#include <sys/wait.h>

#define MESSAGE_SIZE 2048

#define MAX_QA 250

#define SERVER_BACKLOG 10

#define CHAT_LOG_FILE "chat.log"

#define FILE_INPUT "gpt_2_gen_input.txt"
#define FILE_OUTPUT "gpt_2_gen_output.txt"

#define COMMAND_ACTIVE "/active"
#define COMMAND_SEND "/send"
#define COMMAND_LOGOUT "/logout"
#define COMMAND_HISTORY "/history"
#define COMMAND_HISTORY_DELETE "/history_delete"
#define COMMAND_DELETE_ALL "/delete_all"
#define COMMAND_CHATBOT "/chatbot"
#define COMMAND_CHATBOT_LOGOUT "/chatbot logout"
#define COMMAND_CHATBOT_V2 "/chatbot_v2"
#define COMMAND_CHATBOT_V2_LOGOUT "/chatbot_v2 logout"

#define ACK_INVALID_COMMAND "Invalid command."
#define ACK_INVALID_DESTINATION_ID "Invalid destination ID."
#define ACK_MAXIMUM_CLIENT_LIMIT_REACHED "Maximum client limit reached."
#define ACK_LOGOUT_MESSAGE "Bye!! Have a nice day"
#define ACK_WELCOME_MESSAGE "Welcome to the chat server client %d"
#define ACK_CHAT_HISTORY_NOT_FOUND "Chat history not found."
#define ACK_ALL_CHAT_HISTORY_DELETED "All chat history deleted."
#define ACK_CHAT_HISTORY_DELETED "Chat history deleted."

#define CHATBOT_PREPEND_MESSAGE "stupidbot> "
#define CHATBOT_INVALID_COMMAND_MESSAGE "System Malfunction, I couldnot understand your query."
#define CHATBOT_LOGIN_MESSAGE "Hi, I am stupid bot, I am able to answer a limited set of your questions"
#define CHATBOT_LOGOUT_MESSAGE "Bye, Have a nice day and do not complain about me"

#define CHATBOT_V2_PREPEND_MESSAGE "gpt2bot> "
#define CHATBOT_V2_LOGIN_MESSAGE "Hi, I am updated bot, I am able to answer any question be it correct or incorrect"
#define CHATBOT_V2_LOGOUT_MESSAGE "Bye! Have a nice day and hope you do not have any complaints about me"

// Structure to store the client details
typedef struct clientDetail {
    int id;
    int socketFD;
    // 1 - chatting with chatbot, 0 - not chatting with chatbot, 2 - chatting with GPT
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

    printf("Client details initialized.\n");
}

void refreshHistoryFile() {
    FILE *file = fopen(CHAT_LOG_FILE, "w");
    if (file == NULL) {
        perror("Error in opening file.");
        exit(1);
    }
    fclose(file);
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

// Function to convert the string to lower case
char* convertStringToLower (char* s) {
    for (int i = 0; i < strlen(s); ++i)
        if (s[i] >= 'A' && s[i] <= 'Z')
            s[i] += 'a' - 'A';
    return s;
}

int getClientId(int clientSocket) {
    for (int i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->socketFD == clientSocket) {
            return clientDetails[i]->id;
        }
    }
    return -1;
}

int getClientSocket(int clientId) {
    for (int i = 0; i < SERVER_BACKLOG; i++) {
        if (clientDetails[i]->id == clientId) {
            return clientDetails[i]->socketFD;
        }
    }
    return -1;
}

// Function to store the chat history
void storeChatHistory(int sourceId, int destId, char *message) {
    FILE *file = fopen(CHAT_LOG_FILE, "a");
    if (file == NULL) {
        perror("Error in opening file.");
        exit(1);
    }

    char buffer[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    // for source
    sprintf(buffer, "%d %d %d %s\n", sourceId, sourceId, destId, message);
    fprintf(file, "%s", buffer);
    // for destination
    sprintf(buffer, "%d %d %d %s\n", destId, sourceId, destId, message);
    fprintf(file, "%s", buffer);
    fclose(file);
}

// Function to send the chat history
void sendChatHistory(int sourceId, int destId) {
    FILE *file = fopen(CHAT_LOG_FILE, "r");
    if (file == NULL) {
        perror("Error in opening file.");
        exit(1);
    }

    char line[MESSAGE_SIZE];
    char buffer[MESSAGE_SIZE];
    bzero(buffer, MESSAGE_SIZE);
    int flag = 0;

    while (fgets(line, sizeof(line), file) != NULL) {
        line[strcspn(line, "\n")] = 0;
        int sId, dId, source, dest;
        char message[MESSAGE_SIZE];
        bzero(message, MESSAGE_SIZE);
        sscanf(line, "%d %d %d %[^\n]", &sId, &source, &dest, message);

        // remove new line character from the message
        message[strcspn(message, "\n")] = 0;

        // remove leading and trailing spaces
        char *messageTrimmed = trimString(message);

        // chat history messsages send from source to destination
        if (sId == sourceId && dest == destId) {
            flag = 1;
            bzero(buffer, MESSAGE_SIZE);
            sprintf(buffer, "From:%d To:%d Message:%s\n", source, dest, messageTrimmed);
            sendAcknowledgementToClient(getClientSocket(sourceId), buffer);
        }
        // chat history messages send from destination to source
        else if (sId == sourceId && source == destId) {
            flag = 1;
            bzero(buffer, MESSAGE_SIZE);
            sprintf(buffer, "From:%d To:%d Message:%s\n", source, dest, messageTrimmed);
            sendAcknowledgementToClient(getClientSocket(sourceId), buffer);
        }
    }

    if (flag == 0) {
        sendAcknowledgementToClient(getClientSocket(sourceId), ACK_CHAT_HISTORY_NOT_FOUND);
    }

    fclose(file);
}

// Function to delete the chat history
void deleteChatHistory(int sourceId, int destId) {
    FILE *file = fopen(CHAT_LOG_FILE, "r");
    if (file == NULL) {
        perror("Error in opening file.");
        exit(1);
    }

    FILE *tempFile = fopen("temp.txt", "w");
    if (tempFile == NULL) {
        perror("Error in opening file.");
        exit(1);
    }

    char line[MESSAGE_SIZE];
    int flag = 0;

    while (fgets(line, sizeof(line), file) != NULL) {
        line[strcspn(line, "\n")] = 0;
        int sId, dId, source, dest;
        char *message = NULL;
        sscanf(line, "%d %d %d", &sId, &source, &dest);
        message = strtok(NULL, "\0");
        if (sId == sourceId && dest == destId) {
            flag = 1;
        } 
        else if(sId == sourceId && source == destId) {
            flag = 1;
        }
        else {
            fprintf(tempFile, "%s\n", line);
        }
    }

    fclose(file);
    fclose(tempFile);

    remove(CHAT_LOG_FILE);
    rename("temp.txt", CHAT_LOG_FILE);

    if (flag == 1) {
        sendAcknowledgementToClient(getClientSocket(sourceId), ACK_CHAT_HISTORY_DELETED);
    } else {
        sendAcknowledgementToClient(getClientSocket(sourceId), ACK_CHAT_HISTORY_NOT_FOUND);
    }
}

// Function to delete all the chat history
void deleteAllChatHistory(int clientId) {
    FILE *file = fopen(CHAT_LOG_FILE, "r");
    if (file == NULL) {
        perror("Error in opening file.");
        exit(1);
    }

    FILE *tempFile = fopen("temp.txt", "w");
    if (tempFile == NULL) {
        perror("Error in opening file.");
        exit(1);
    }

    char line[MESSAGE_SIZE];
    int flag = 0;

    while (fgets(line, sizeof(line), file) != NULL) {
        line[strcspn(line, "\n")] = 0;
        int sId, dId, source, dest;
        char *message = NULL;
        sscanf(line, "%d %d %d", &sId, &source, &dest);
        message = strtok(NULL, "\0");
        if (sId == clientId) {
            flag = 1;
        } else {
            fprintf(tempFile, "%s\n", line);
        }
    }

    fclose(file);
    fclose(tempFile);

    remove(CHAT_LOG_FILE);
    rename("temp.txt", CHAT_LOG_FILE);

    if (flag == 1) {
        sendAcknowledgementToClient(getClientSocket(clientId), ACK_ALL_CHAT_HISTORY_DELETED);
    } else {
        sendAcknowledgementToClient(getClientSocket(clientId), ACK_CHAT_HISTORY_NOT_FOUND);
    }
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
    return id;
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

    // Removing the chat history of the client
    deleteAllChatHistory(id);

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
    if (strcmp(question, COMMAND_CHATBOT_LOGOUT) == 0) {
        setChatBotStatusOfClient(clientSocket, 0);
        char buffer[MESSAGE_SIZE];
        bzero(buffer, MESSAGE_SIZE);
        sprintf(buffer, "%s%s", CHATBOT_PREPEND_MESSAGE, CHATBOT_LOGOUT_MESSAGE);
        sendAcknowledgementToClient(clientSocket, buffer);
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
        char buffer[MESSAGE_SIZE];
        bzero(buffer, MESSAGE_SIZE);
        sprintf(buffer, "%s%s", CHATBOT_PREPEND_MESSAGE, CHATBOT_INVALID_COMMAND_MESSAGE);
        sendAcknowledgementToClient(clientSocket, buffer);
    } else {
        // apppend 'stupidbot>' at the beginning of the answer
        char buffer[MESSAGE_SIZE];
        bzero(buffer, MESSAGE_SIZE);
        sprintf(buffer, "%s%s", CHATBOT_PREPEND_MESSAGE, answer);
        sendAcknowledgementToClient(clientSocket, buffer);
    }
}

// Function to make the call to python file to get data
char *makingTheCallToPythonFile(char *question) {

    // writing the question to the file
    FILE *file = fopen(FILE_INPUT, "w");
    if (file == NULL) {
        perror("Error in opening file.");
        exit(1);
    }
    fprintf(file, "%s", question);
    fclose(file);

    // calling the python file
    pid_t pid = fork();
    if (pid == 0) {
        execlp("python3", "python3", "gpt_2_gen.py", NULL);
    }
    wait(NULL);

    // reading the output from the file
    file = fopen(FILE_OUTPUT, "r");
    if (file == NULL) {
        perror("Error in opening file.");
        exit(1);
    }

    char line[MESSAGE_SIZE];
    char *answer = NULL;

    while (fgets(line, MESSAGE_SIZE, file) != NULL) {
        line[strcspn(line, "\n")] = 0;
        // remove leading and trailing spaces
        answer = trimString(line);
    }

    fclose(file);

    return answer;
}

// Function to handle the chatbot for GPT
void chatbotHandlerForGPT(char *request, int clientSocket) {
    char *question = trimString(request);
    char *answer = NULL;
    int flag = 0;

    // If /chatbot_v2 logout is entered, then set the chatbot status to 0
    if (strcmp(question, COMMAND_CHATBOT_V2_LOGOUT) == 0) {
        setChatBotStatusOfClient(clientSocket, 0);
        char buffer[MESSAGE_SIZE];
        bzero(buffer, MESSAGE_SIZE);
        sprintf(buffer, "%s%s", CHATBOT_V2_PREPEND_MESSAGE, CHATBOT_V2_LOGOUT_MESSAGE);
        sendAcknowledgementToClient(clientSocket, buffer);
        return;
    }

    // If the question is not empty, then send the question to the GPT model
    if (strlen(question) > 0) {
        answer = makingTheCallToPythonFile(question);
        flag = 1;
    }

    if (flag == 0) {
        char buffer[MESSAGE_SIZE];
        bzero(buffer, MESSAGE_SIZE);
        sprintf(buffer, "%s%s", CHATBOT_V2_PREPEND_MESSAGE, CHATBOT_INVALID_COMMAND_MESSAGE);
        sendAcknowledgementToClient(clientSocket, buffer);
    } else {
        char buffer[MESSAGE_SIZE];
        bzero(buffer, MESSAGE_SIZE);
        // copy the prefix and answer to the buffer
        strcpy(buffer, CHATBOT_V2_PREPEND_MESSAGE);
        strcat(buffer, answer);
        sendAcknowledgementToClient(clientSocket, buffer);
    }
}

// Function to handle the client request
int handleClientRequest(int clientSocket, char *request) {
    int chatbotStatus = getChatBotStatusOfClient(clientSocket);

    // remove leading and trailing spaces and convert to lowercase
    request = trimString(request);
    request = convertStringToLower(request);

    if (chatbotStatus == 1) {
        chatbotHandler(request, clientSocket);
        return 0;
    }
    else if (chatbotStatus == 2) {
        chatbotHandlerForGPT(request, clientSocket);
        return 0;
    }

    // printf("Request : %s\n", request);

    char *command = strtok(request, " ");
    printf("Command : %s\n", command);
    if (command == NULL) {
        sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND);
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

        // store the chat history for botht the clients
        storeChatHistory(sourceId, atoi(destId), message);
    } else if (strcmp(command, COMMAND_LOGOUT) == 0) {
        sendAcknowledgementToClient(clientSocket, ACK_LOGOUT_MESSAGE);
        return -1;
    } else if (strcmp(command, COMMAND_CHATBOT) == 0) {
        char *subCommand = strtok(NULL, "");
        if (strcmp(subCommand, "login") == 0) {
            setChatBotStatusOfClient(clientSocket, 1);
            // prepending the message
            char buffer[MESSAGE_SIZE];
            bzero(buffer, MESSAGE_SIZE);
            sprintf(buffer, "%s%s", CHATBOT_PREPEND_MESSAGE, CHATBOT_LOGIN_MESSAGE);
            sendAcknowledgementToClient(clientSocket, buffer);
        } else {
            sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND);
        }
        return 0;
    } else if (strcmp(command, COMMAND_HISTORY) == 0) {
        char *destId = strtok(NULL, "");
        if (destId == NULL) {
            sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND);
            return 0;
        }

        int destClientId = atoi(destId);
        printf("Dest Id: %s\n", destId);
        sendChatHistory(getClientId(clientSocket), destClientId);
    } else if (strcmp(command, COMMAND_HISTORY_DELETE) == 0) {
        char *destId = strtok(NULL, " ");
        if (destId == NULL) {
            sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND);
            return 0;
        }

        int destClientId = atoi(destId);
        deleteChatHistory(getClientId(clientSocket), destClientId);
    } else if (strcmp(command, COMMAND_DELETE_ALL) == 0) {
        deleteAllChatHistory(getClientId(clientSocket));
    }
    // Clients should be able to toggle the chatbot feature using commands
    // ○ "/chatbot_v2 login" - to avail the chatbot feature
    // ○ "/chatbot_v2 logout" - to disable the feature
    else if (strcmp(command, COMMAND_CHATBOT_V2) == 0) {
        char *subCommand = strtok(NULL, "");
        if (subCommand == NULL) {
            sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND);
            return 0;
        }

        if (strcmp(subCommand, "login") == 0) {
            setChatBotStatusOfClient(clientSocket, 2);
            // prepending the message
            char buffer[MESSAGE_SIZE];
            bzero(buffer, MESSAGE_SIZE);
            sprintf(buffer, "%s%s", CHATBOT_V2_PREPEND_MESSAGE, CHATBOT_V2_LOGIN_MESSAGE);
            sendAcknowledgementToClient(clientSocket, buffer);
        } else {
            sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND);
        }
    }
    else {
        sendAcknowledgementToClient(clientSocket, ACK_INVALID_COMMAND);
    }

    return 0;
}

void main(int argc, char *argv[]) {
    // Loading the chatbot data
    initializeClientDetailsAndChatBot();
    loadChatbot();
    refreshHistoryFile();

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
                        bzero(buf, MESSAGE_SIZE);
                        // send the client id to the client
                        sprintf(buf, ACK_WELCOME_MESSAGE, status);
                        sendAcknowledgementToClient(newfd, buf);
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