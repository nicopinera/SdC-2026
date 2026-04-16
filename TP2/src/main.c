#include <stdio.h>
#include <stdlib.h>

int cast(float x) {
  int val = (int)x;
  return val + 1;
}

int main(void) {
  int a = cast(7.4);
  printf("%d", a);

  return EXIT_SUCCESS;
}
