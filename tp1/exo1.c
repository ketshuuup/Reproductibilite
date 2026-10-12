#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int main(void) {
    srand(time(NULL));

    int marche =0;

    for (int i = 1; i <= 1000001; i++) {
        float y = (float)rand() / (float)RAND_MAX;
        float x = (float)rand() / (float)RAND_MAX;
        float z = (float)rand() / (float)RAND_MAX;
        if ((x + y) + z == x + (y + z) ) {
            marche++;
        }

    }


    printf("N = %d\n", marche);
    return 0;
}
