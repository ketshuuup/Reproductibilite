#include <stdio.h>
#include <math.h>

int main(void) {
    double gain = exp(1.0) - 1;
    for (int i = 1; i <= 50; i++) {
        gain = gain * i - 1;
    }

    FILE *f = fopen("/home/amine/Desktop/Reproductibilite/tp1/EXO2.txt", "w"); //ICI AUSSI TU MODIFIE LE CHEMIN SELON TON ORDIE
    if (f == NULL) {
        perror("EXO2.txt");
        return 1;
    }
    fprintf(f, "%f\n", gain);
    fclose(f);

    return 0;
}