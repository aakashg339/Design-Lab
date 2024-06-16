#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void main() {
    char text1[50];
    char text2[] = "temp";
    char text3[] = "tempo this world";

    printf("%d\n", strcmp(text2, text3));
    printf("%d\n", strncmp(text2, text3, strlen(text2)));

    printf("%d\n", memcmp(text2, text3, strlen(text2)));

    int arr1[] = {1,2,3};
    int arr2[] = {1,2,4};

    printf("%d\n", memcmp(arr1, arr2, sizeof(arr1)));
}