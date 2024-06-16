#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define STRING_SIZE 256

// Function to convert string to binary
void convertStringToBinary(char *inputString, char *binaryString) {
    int i, j;
    char ch;
    for (i = 0; i < strlen(inputString); i++) {
        ch = inputString[i];
        for(j=7; j>=0; j--) {
            if(ch >= (1 << j)) {
                ch -= (1 << j);
                binaryString[(i * 8) + (7 - j)] = '1';
            } else {
                binaryString[(i * 8) + (7 - j)] = '0';
            }
        }
    }
}

void main() {
    char *inputString = (char *)malloc(STRING_SIZE * (sizeof(char)));
    char *binaryString = (char *)malloc(STRING_SIZE * (sizeof(char) * 8));

    printf("Enter a string: ");
    // reading the entire line

    fgets(inputString, STRING_SIZE, stdin);

    // Remove the newline character
    inputString[strlen(inputString) - 1] = '\0';

    // Convert string to binary
    convertStringToBinary(inputString, binaryString);

    printf("\nBinary form of the string: %s\n", binaryString);

    free(inputString);
    free(binaryString);
}