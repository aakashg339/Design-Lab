#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// CRC-32 Lookup Table
unsigned int crc_table[256];

// Initialize CRC Lookup Table
void init_crc_table() {
    unsigned int crc;
    int i, j;

    for (i = 0; i < 256; i++) {
        crc = i;
        for (j = 0; j < 8; j++) {
            crc = (crc & 1) ? (crc >> 1) ^ 0xEDB88320UL : (crc >> 1);
        }
        crc_table[i] = crc;
    }
}

// Calculate CRC-32 for a given data block
unsigned int calculate_crc(const unsigned char *data, size_t data_len) {
    unsigned int crc = 0xFFFFFFFFUL;
    size_t i;

    for (i = 0; i < data_len; i++) {
        crc = (crc >> 8) ^ crc_table[(crc & 0xFF) ^ data[i]];
    }

    return crc ^ 0xFFFFFFFFUL;
}

// Convert string to binary form
void string_to_binary(const char *str, unsigned char *binary) {
    size_t i;
    for (i = 0; i < strlen(str); i++) {
        binary[i] = (unsigned char)str[i];
        printf("%c: %c\n", str[i], binary[i]);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s string1 string2\n", argv[0]);
        return 1;
    }

    init_crc_table();

    // Convert strings to binary form
    unsigned char binary1[256];
    unsigned char binary2[256];
    string_to_binary(argv[1], binary1);
    string_to_binary(argv[2], binary2);

    printf("Binary 1: %s\n", binary1);
    printf("Binary 2: %s\n", binary2);

    // Calculate CRC for each string
    unsigned int crc1 = calculate_crc(binary1, strlen(argv[1]));
    unsigned int crc2 = calculate_crc(binary2, strlen(argv[2]));

    printf("CRC 1: %u\n", crc1);
    printf("CRC 2: %u\n", crc2);

    // Check for errors
    if (crc1 == crc2) {
        printf("No error detected. CRC values for both strings match.\n");
        return 0; // No error
    } else {
        printf("Error detected. CRC values for the two strings do not match.\n");
        return 1; // Error
    }
}

