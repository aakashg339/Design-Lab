#include<stdio.h>
#include<string.h>
#include<stdlib.h>

void main(int argc, char *argv[]) {
    // char str[] = {'H', 'e', 'l', 'l', 'l', 'o', '\0'}; // Below is actually doing this. They are same.
    // char str[] = "Hello";
    // printf("%s\n", str);
    // str[0] = 'h';
    // printf("%s\n", str);

    // const static char noname[] = "Hello";
    // char str2 = noname;
    // char *str2 = "Hello"; // THis line is actually doing above 
    // printf("%s\n", str2);
    // Below will result in error
    // str2[0] = 'h';
    // printf("%s\n", str2);

    char *str3 = malloc(50 * sizeof(char));
    if (str3 == NULL) {
        printf("Error");
    }
    strcpy(str3, "Hello"); 
    printf("%s\n", str3);
    str3[0] = 'h';
    printf("%s\n", str3);
    free(str3);
}