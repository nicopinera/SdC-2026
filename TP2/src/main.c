#include <stdio.h>
#include <stdlib.h>

int castear_datos(float x) {

  int val = (int)x + 1;
  return val;
}

int main() {
  FILE *file = fopen("data/Argentina.txt", "r");
  if (file == NULL) {
    perror("Error al abrir el archivo");
    return 1;
  }

  int anio;
  float gini;

  while (fscanf(file, "%d - %f", &anio, &gini) == 2) {
    int resultado = castear_datos(gini);
    printf("Año: %d | Gini original: %.2f | Procesado: %d\n", anio, gini,
           resultado);
  }

  fclose(file);
  return EXIT_SUCCESS;
}
