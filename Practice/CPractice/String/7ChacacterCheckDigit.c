#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void main() {
    char c = 48; // '0'. 48 = '0'
    if (c>=48 && c<=57)
        printf("This is a number");
    else
        printf("This is not a number");
}