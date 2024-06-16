#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void main() {
    char str[] = "Hello, friend";
    
    // to get first occurance
    // char *result = strchr(str, ',');
    // To get last occurance
    char *result = strrchr(str, 'e');
    int pos = (result - str);

    if(result)
        printf("Character was found at pos %d", pos);
    else
        printf("Character was not found");
}