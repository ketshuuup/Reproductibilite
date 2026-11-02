 Is (x+y)+z == x+(y+z)? How often? Write a program in C that prints a percentage.

The question is under-specified ("x, y, z: number"), so make choices and write each one down.

To answer this question precisely, we first need to address the under-specification by making explicit choices about what "x, y, z: number" means in terms of math versus computer science.
Making Choices & Assumptions

    Choice 1: Mathematical Real/Integer Numbers (R or Z)

        Rule: Addition is strictly associative.

        Result: (x+y)+z=x+(y+z) is always true (100% of the time).

    Choice 2: Computer Floating-Point Numbers (IEEE 754 float)

        Rule: Due to finite precision and rounding errors in computers, floating-point addition is not always associative.

        Result: Because testing every possible 32-bit float combination (232×232×232) is computationally impossible, we will estimate the percentage using random sampling over a standard numerical range.

C Program for Floating-Point Associativity

The C program below generates random float values within a specified range, tests the associative property, and prints the percentage of cases where they are equal.
C

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    long long total_samples = 10000000; // 10 million samples
    long long equal_count = 0;
    
    // Seed the random number generator
    srand((unsigned int)time(NULL));
    
    for (long long i = 0; i < total_samples; i++) {
        // Generate random floats between -1000.0 and 1000.0
        float x = ((float)rand() / RAND_MAX) * 2000.0f - 1000.0f;
        float y = ((float)rand() / RAND_MAX) * 2000.0f - 1000.0f;
        float z = ((float)rand() / RAND_MAX) * 2000.0f - 1000.0f;
        
        float left = (x + y) + z;
        float right = x + (y + z);
        
        // Check exact equality
        if (left == right) {
            equal_count++;
        }
    }
    
    double percentage = ((double)equal_count / total_samples) * 100.0;
    
    printf("Total Samples Tested: %lld\n", total_samples);
    printf("Equal Count: %lld\n", equal_count);
    printf("Percentage where (x+y)+z == x+(y+z): %.2f%%\n", percentage);
    
    return 0;
}

Expected Output Summary

When running this program with standard single-precision floats (float), you will typically find that equality holds in roughly 75% to 85% of random samples depending on the magnitude of the numbers and distribution range, demonstrating that floating-point arithmetic frequently breaks mathematical associativity.

Would you like to explore how double-precision (double) changes these results?
