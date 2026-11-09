#include <stdio.h>
#include <stdlib.h>

typedef double real;

int main(int argc, char **argv) {
    int repetitions = 1000;
    unsigned int seed = 1;
    double low = 0.0, high = 1.0;
    for (int i = 1; i < argc; i++) {
        sscanf(argv[i], "--repetitions=%d", &repetitions);
        sscanf(argv[i], "--seed=%u", &seed);
        sscanf(argv[i], "--low=%lf", &low);
        sscanf(argv[i], "--high=%lf", &high);
    }
    srand(seed);
    real lo = (real)low, hi = (real)high;
    long long holds = 0;
    for (int i = 0; i < repetitions; i++) {
        real x = lo + (hi - lo) * ((real)rand() / (real)RAND_MAX);
        real y = lo + (hi - lo) * ((real)rand() / (real)RAND_MAX);
        real z = lo + (hi - lo) * ((real)rand() / (real)RAND_MAX);
        if (x * (1 / x) == 1) holds++;
    }
    printf("%.4f\n", 100.0 * holds / repetitions);
    return 0;
}