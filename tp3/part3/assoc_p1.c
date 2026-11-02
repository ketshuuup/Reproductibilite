#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int repetitions = 1000000, seed = 42;
    double low = 0.0, high = 1.0;
    for (int i = 1; i < argc; i++) {
        sscanf(argv[i], "--repetitions=%d", &repetitions);
        sscanf(argv[i], "--seed=%d", &seed);
        sscanf(argv[i], "--low=%lf", &low);
        sscanf(argv[i], "--high=%lf", &high);
    }
    srand(seed);
    float lo = (float)low, hi = (float)high;

    long long marche = 0;
    for (int i = 0; i < repetitions; i++) {
        float y = lo + (hi - lo) * ((float)rand() / (float)RAND_MAX);
        float x = lo + (hi - lo) * ((float)rand() / (float)RAND_MAX);
        float z = lo + (hi - lo) * ((float)rand() / (float)RAND_MAX);
        if ((x + y) + z == x + (y + z)) {
            marche++;
        }
    }

    printf("{\"program\": \"P1_C_tp1\", \"repetitions\": %d, \"seed\": %d, \"low\": %g, \"high\": %g, \"percentage\": %.4f}\n",
           repetitions, seed, low, high, 100.0 * marche / repetitions);
    return 0;
}