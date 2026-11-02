#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(void) {
    double gain = exp(1.0) - 1;
    for (int i = 1; i <= 50; i++) {
        gain = gain * i - 1;
    }

    /* dossier de sortie : variable d'environnement OUT_DIR (defaut : dossier courant) */
    const char *out_dir = getenv("OUT_DIR");
    if (out_dir == NULL || out_dir[0] == '\0') out_dir = ".";
    char path[1024];
    snprintf(path, sizeof path, "%s/answer_banking.txt", out_dir);

    FILE *f = fopen(path, "w");
    if (f == NULL) {
        perror(path);
        return 1;
    }
    fprintf(f, "%f\n", gain);
    fclose(f);

    printf("FINALE : %f (ecrit dans %s)\n", gain, path);
    return 0;
}