#include<stdio.h>
#include<string.h>
#include<stdlib.h>

void main(int argc, char *argv[]) {
    // char array[3][50];

    // // strcpy()
    // strcpy(array[0], "Hello world");
    // strcpy(array[1], "test");
    // strcpy(array[2], "123");

    // char array[3][50] = {"Hello world", "test", "123"};

    char array[][50] = {"Hello world", "test", "123"};

    printf("%s\n%s\n%s", array[0], array[1], array[2]);
}