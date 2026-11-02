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
    double lo = (double)low, hi = (double)high;

    long long marche = 0;
    for (int i = 0; i < repetitions; i++) {
        double y = lo + (hi - lo) * ((double)rand() / (double)RAND_MAX);
        double x = lo + (hi - lo) * ((double)rand() / (double)RAND_MAX);
        double z = lo + (hi - lo) * ((double)rand() / (double)RAND_MAX);
        if ((x + y) + z == x + (y + z)) {
            marche++;
        }
    }

    printf("{\"program\": \"P1_C_tp1\", \"repetitions\": %d, \"seed\": %d, \"low\": %g, \"high\": %g, \"percentage\": %.4f}\n",
           repetitions, seed, low, high, 100.0 * marche / repetitions);
    return 0;
}