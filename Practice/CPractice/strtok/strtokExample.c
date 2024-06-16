#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main () {
    int day, year;
    char weekday[20], month[20], dtm[100];
    char line[1024];
    
    strcpy(line, "7777 7777 6848 Hello How are you?");
    
    line[strcspn(line, "\n")] = 0;
    int sId, dId, source, dest;
    char *message = NULL;
    sscanf(line, "%d %d %d", &sId, &source, &dest);
    message = strtok(line, "\0");
    message = strtok(message, " ");
    message = strtok(NULL, " ");
    message = strtok(NULL, " ");
    message = strtok(NULL, "\0"); // This will get the message
    
    printf("\n%d", sId);
    
    printf("\n%d", source);
    
    printf("\n%d", dest);
    
    printf("\nMessage=%s", message);

   return(0);
}