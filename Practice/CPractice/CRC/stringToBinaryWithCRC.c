#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define STRING_SIZE 256

void XOR(char *check_value, char *gen_poly, int N) {
    int j;
    // if both bits are the same, the output is 0
    // if the bits are different the output is 1
    for(j = 1;j < N; j++)
        check_value[j] = (( check_value[j] == gen_poly[j])?'0':'1');

}

void crc(char *data, char *check_value, char *gen_poly, int N, int data_length) {
    int i, j;
    // initializing check_value
    for(i=0;i<N;i++)
        check_value[i]=data[i];

    // printf("\n----------------------------------------");
    // printf("\nInitial check value: %s", check_value);
    do{
    // check if the first bit is 1 and calls XOR function
        if(check_value[0]=='1')
            XOR(check_value, gen_poly, N);
// Move the bits by 1 position for the next computation
        for(j=0;j<N-1;j++)
            check_value[j]=check_value[j+1];
        // appending a bit from data
        check_value[j]=data[i++];
        // printf("\nCheck value: %s", check_value);
    }while(i<=data_length+N-1);
// loop until the data ends
}

// Function to check for errors on the receiver side
void receiver(char *data, char *check_value, char *gen_poly, int N) {
    int i;
    // get the received data
    printf("Enter the received data: ");
    scanf("%s", data);
    printf("\n-----------------------------\n");
    printf("Data received: %s", data);
    // Cyclic Redundancy Check
    crc(data, check_value, gen_poly, N, strlen(data));
    // Check if the remainder is zero to find the error
    for(i=0;(i<N-1) && (check_value[i]!='1');i++);
        if(i<N-1)
            printf("\nError detected\n\n");
        else
            printf("\nNo error detected\n\n");
}

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

    binaryString[i * 8] = '\0';
}

void main() {
    char *inputString = (char *)malloc(STRING_SIZE * (sizeof(char)));
    char *binaryString = (char *)malloc(STRING_SIZE * (sizeof(char) * 8));
    char gen_poly[10];

    printf("Enter a string: ");
    // reading the entire line

    fgets(inputString, STRING_SIZE, stdin);

    // Remove the newline character
    inputString[strlen(inputString) - 1] = '\0';

    // // Convert string to binary
    // convertStringToBinary(inputString, binaryString);

    strcpy(binaryString, inputString);

    printf("\nBinary form of the string: %s\n", binaryString);

    // generator polynomial
    printf("\nEnter the Generating polynomial: ");
    // get the generator polynomial
    scanf("%s",gen_poly);

    // variables
    int data_length,i,j;
    char *check_value = (char *)malloc(STRING_SIZE * (sizeof(char) * 8));
    int N = strlen(gen_poly);

    // find the length of data
    data_length=strlen(binaryString);

    // appending n-1 zeros to the data
    for(i=data_length;i<data_length+N-1;i++)
        binaryString[i]='0';

    // Printing the binary string character by character
    // for(i=0;i<data_length+N;i++)
    //     printf("%c,", binaryString[i]);

    // print the data with padded zeros
    printf("\n Data padded with n-1 zeros : %s", binaryString);
    printf("\n----------------------------------------");

    crc(binaryString, check_value, gen_poly, N, data_length);

    // print the computed check value
    printf("\nCRC or Check value is : %s",check_value);

    // Append data with check_value(CRC)  
    for(i=data_length;i<data_length+N-1;i++)
        binaryString[i]=check_value[i-data_length];

    printf("\n----------------------------------------");
    // printing the final data to be sent
    printf("\n Final data to be sent : %s", binaryString);
    printf("\n----------------------------------------\n");

    receiver(binaryString, check_value, gen_poly, N);

    free(inputString);
    free(binaryString);

    return;
}