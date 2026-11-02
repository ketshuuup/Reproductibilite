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
