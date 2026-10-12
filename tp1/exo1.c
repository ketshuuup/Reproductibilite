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

    /* dossier de sortie : variable d'environnement OUT_DIR (défaut : dossier courant) */
    const char *out_dir = getenv("OUT_DIR");
    if (out_dir == NULL || out_dir[0] == '\0') out_dir = ".";

    char path[1024];
    snprintf(path, sizeof path, "%s/answer_associativity.txt", out_dir);

    FILE *f = fopen(path, "w");
    if (f == NULL) {
        perror(path);
        return 1;
    }
    fprintf(f, "%d\n", marche);
    fclose(f);
    return 0;
}