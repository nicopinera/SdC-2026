#include <stdio.h>

extern int cast(float); // Funcion implementada en assembler

int procesar_datos(float x) {
  printf("Pasando datos de C a ASM. ");
  printf("Dato obtenido desde python: %f . ", x);
  int valor_entero = cast(x);
  printf("Dato de ASM: %d\n",valor_entero);
  return valor_entero;
}
