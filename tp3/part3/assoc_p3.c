#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char **argv) {
    int repetitions = 10000000, seed = -1;
    double low = -1000.0, high = 1000.0;
    for (int i = 1; i < argc; i++) {
        sscanf(argv[i], "--repetitions=%d", &repetitions);
        sscanf(argv[i], "--seed=%d", &seed);
        sscanf(argv[i], "--low=%lf", &low);
        sscanf(argv[i], "--high=%lf", &high);
        
    }
    if (seed < 0) seed = (int)time(NULL);
    srand((unsigned int)seed);
    float lo = (float)low, hi = (float)high;
    long long equal_count = 0;
    for (int i = 0; i < repetitions; i++) {
        float x = ((float)rand() / RAND_MAX) * (hi - lo) + lo;
        float y = ((float)rand() / RAND_MAX) * (hi - lo) + lo;
        float z = ((float)rand() / RAND_MAX) * (hi - lo) + lo;
        float left = (x + y) + z;
        float right = x + (y + z);
        if (left == right) equal_count++;
    }
    printf("{\"program\": \"P3_C_gemini\", \"repetitions\": %d, \"seed\": %d, \"low\": %g, \"high\": %g, \"percentage\": %.4f}\n",
           repetitions, seed, low, high, 100.0 * equal_count / repetitions);
    return 0;
}