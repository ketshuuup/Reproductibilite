#include <stdio.h>
#include <stdlib.h>

#define N_TRIALS 1000000
#define SEED 42

int main(void) {
    srand(SEED);

    int marche = 0;
    for (int i = 0; i < N_TRIALS; i++) {
        float y = (float)rand() / (float)RAND_MAX;
        float x = (float)rand() / (float)RAND_MAX;
        float z = (float)rand() / (float)RAND_MAX;
        if ((x + y) + z == x + (y + z)) {
            marche++;
        }
    }

    FILE *f = fopen("/home/amine/Desktop/Reproductibilite/tp1/EXO1.txt", "w"); //BIEN SURE TU MODIFIE LE CHEMIN FAIT PAS LE CON AUSSI
    if (f == NULL) {
        perror("answer_associativity.txt");
        return 1;
    }
    fprintf(f, "%d\n", marche);
    fclose(f);
    return 0;
}