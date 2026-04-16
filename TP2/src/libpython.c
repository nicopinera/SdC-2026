#include <stdio.h>

extern int cast(float); // Funcion implementada en assembler

int procesar_datos(float x) {
  printf("Pasando datos de C a ASM...\n");
  printf("Dato obtenido desde python: %f\n", x);
  int valor_entero = cast(x);
  return valor_entero;
}
