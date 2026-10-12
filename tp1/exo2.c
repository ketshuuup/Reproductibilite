#include <stdio.h>
#include <math.h>

int main(void) {

    double gain = exp(1.0) - 1;
    for (int i = 1; i <= 50; i++) {
        gain = gain * i - 1;
    }

    printf("FINALE : %f\n", gain);
    return 0;
}