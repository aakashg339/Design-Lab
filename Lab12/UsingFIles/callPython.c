#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#define FILE_INPUT "gpt_2_gen_input.txt"
#define FILE_OUTPUT "gpt_2_gen_output.txt"
#define MESSAGE_SIZE 1000

#define CHATBOT_V2_PREPEND_MESSAGE "gpt2bot> "



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

    while (fgets(line, sizeof(line), file) != NULL) {
        line[strcspn(line, "\n")] = 0;
        answer = line;
    }

    fclose(file);

    return answer;
}

char *onlyReadOutputFile() {
    FILE *file = fopen(FILE_OUTPUT, "r");
    char *answer = NULL;
    if (file == NULL) {
        perror("Error in opening file.");
        exit(1);
    }

    char line[MESSAGE_SIZE];
    while (fgets(line, sizeof(line), file) != NULL) {
        line[strcspn(line, "\n")] = 0;
        answer = line;
    }

    fclose(file);

    return answer;
}

int main() {
    char question[MESSAGE_SIZE];
    char *answer;
    int flag = 0;
    // printf("Enter the question: ");
    // fgets(question, MESSAGE_SIZE, stdin);

    // If the question is not empty, then send the question to the GPT model
    // if (strlen(question) > 0) {
    //     answer = onlyReadOutputFile();
    //     flag = 1;
    // }

    answer = onlyReadOutputFile();
    flag = 1;

    printf("Answer: %s\n", answer);

    if (flag == 1) {
        // apppend 'gpt2bot>' at the beginning of the answer
        printf("Answer: %s\n", answer);
        // length of the answer
        printf("Length of the answer: %ld\n", strlen(answer));
        char buffer[MESSAGE_SIZE];
        bzero(buffer, MESSAGE_SIZE);
        sprintf(buffer, "%s%s", CHATBOT_V2_PREPEND_MESSAGE, answer);
        printf("Answer: %s\n", buffer);
        printf("Length of the answer: %ld\n", strlen(buffer));
    }

    // 

    return 0;
}