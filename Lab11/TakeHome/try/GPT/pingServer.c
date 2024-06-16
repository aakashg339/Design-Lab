#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/time.h>

#define PORT 12345
#define MAX_CLIENTS 10
#define BUFFER_SIZE 1024
#define UUID_STR_LEN 10  // Simplified for demonstration

typedef struct {
    int sock;
    char id[UUID_STR_LEN];  // Simulated unique IDs
    int chatbot_active;
} client_t;

client_t clients[MAX_CLIENTS];
int client_count = 0;

void add_client(int sock, fd_set* all_sockets, int* max_fd) {
    if (client_count >= MAX_CLIENTS) {
        char* message = "Server is full. Try again later.\n";
        send(sock, message, strlen(message), 0);
        close(sock);
        return;
    }

    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (clients[i].sock == 0) {  // Assuming 0 means unused
            clients[i].sock = sock;
            snprintf(clients[i].id, UUID_STR_LEN, "%d", i + 1);  // Simulated unique ID
            printf("Assigned ID %s to new connection\n", clients[i].id);
            FD_SET(sock, all_sockets);
            if (sock > *max_fd) {
                *max_fd = sock;
            }
            client_count++;
            break;
        }
    }
}

void remove_client(int sock, fd_set* all_sockets, int* max_fd) {
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (clients[i].sock == sock) {
            printf("Client ID %s disconnected\n", clients[i].id);
            FD_CLR(sock, all_sockets); // Remove from fd_set
            clients[i].sock = 0; // Mark as unused
            client_count--;
            close(sock); // Close the socket

            // If the disconnecting client had the highest file descriptor, find the new max
            if (sock == *max_fd) {
                *max_fd = 0;
                for (int j = 0; j < MAX_CLIENTS; j++) {
                    if (clients[j].sock > *max_fd) {
                        *max_fd = clients[j].sock;
                    }
                }
            }
            break;
        }
    }
}

void handle_command(int client_sock, char* buffer, fd_set* all_sockets, int* max_fd) {
    if (strncmp(buffer, "/active", 7) == 0) {
        char activeList[BUFFER_SIZE] = "Active clients: ";
        for (int i = 0; i < MAX_CLIENTS; i++) {
            if (clients[i].sock != 0) {
                strcat(activeList, clients[i].id);
                strcat(activeList, " ");
            }
        }
        send(client_sock, activeList, strlen(activeList), 0);
    }
    else if (strncmp(buffer, "/logout", 7) == 0) {
        char message[BUFFER_SIZE] = "Bye! Have a nice day.\n";
        send(client_sock, message, strlen(message), 0); // Send goodbye message
        remove_client(client_sock, all_sockets, max_fd); // Cleanly remove client
    }
}

void process_client_message(int client_sock, char* buffer, fd_set* all_sockets, int* max_fd) {
    if (buffer[0] == '/') {
        handle_command(client_sock, buffer, all_sockets, max_fd);
    } else {
        printf("Message from client: %s\n", buffer);
    }
}

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
    
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 3) < 0) {
        perror
        ("listen");
        exit(EXIT_FAILURE);
    }

    fd_set current_sockets, ready_sockets;
    FD_ZERO(&current_sockets);
    FD_SET(server_fd, &current_sockets);
    int max_fd = server_fd;

    while (1) {
        ready_sockets = current_sockets;
        if (select(max_fd + 1, &ready_sockets, NULL, NULL, NULL) < 0) {
            perror("select error");
            exit(EXIT_FAILURE);
        }

        for (int i = 0; i <= max_fd; i++) {
            if (FD_ISSET(i, &ready_sockets)) {
                if (i == server_fd) {
                    // Handle new connection
                    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
                        perror("accept");
                        continue;
                    }

                    printf("New connection: socket fd is %d, ip is: %s, port: %d\n", new_socket, inet_ntoa(address.sin_addr), ntohs(address.sin_port));
                    add_client(new_socket, &current_sockets, &max_fd);
                } else {
                    // Handle data from clients
                    char buffer[BUFFER_SIZE];
                    int valread = read(i, buffer, BUFFER_SIZE - 1);
                    if (valread > 0) {
                        buffer[valread] = '\0';
                        process_client_message(i, buffer, &current_sockets, &max_fd);
                    } else if (valread == 0) {
                        // Client disconnected, clean up
                        getpeername(i, (struct sockaddr*)&address, (socklen_t*)&addrlen);
                        printf("Host disconnected, ip %s, port %d\n", inet_ntoa(address.sin_addr), ntohs(address.sin_port));
                        remove_client(i, &current_sockets, &max_fd);
                    } else {
                        perror("read");
                    }
                }
            }
        }
    }

    close(server_fd);
    return 0;
}