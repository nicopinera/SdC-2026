#include <signal.h>
#include <stdio.h>
#include <math.h>

int run = 1;

void handler_keyboard(int sig)
{
    printf("\nSe detiene el programa\n");
    run = 0;
}

int main()
{
    signal(SIGINT, handler_keyboard);
    printf("Hola mundo desde un paquete para Ubuntu\n");
    printf("Para salir presione Ctrl+C\n");
    printf("Esto es una calculadora basica para dos numeros.:\n");
    double a,b,resultado;
    char operacion;
    while (run)
    {
        a = 0;
        b = 0;
        resultado = 0;
        printf("Escriba la operacion a realizar (* + / - ^): ");
        operacion = getchar();
        switch (operacion)
        {
        case '*':
            printf("La opreacion elegida fue MULTIPLICACION\n");
            printf("Ingrese el primer numero: ");
            scanf("%lf", &a);
            printf("Ingrese el segundo numero: ");
            scanf("%lf", &b);
            resultado = a * b;
            printf("El resultado del producto entre %.2f * %.2f es %.2f\n",a,b, resultado);
            break;
        case '+':
            printf("La opreacion elegida fue SUMA\n");
            printf("Igrese el primer sumando : ");
            scanf("%lf", &a);
            printf("Ingrese el segundo sumando: ");
            scanf("%lf", &b);
            resultado = a + b;
            printf("El resultado de la suma de %.2f + %.2f es %.2f\n",a,b, resultado);
            break;
        case '/':
            printf("La opreacion elegida fue DIVISION\n");            
            printf("Ingrese un dividendo: ");
            scanf("%lf", &a);
            printf("Ingrese un divisor (distinto de 0): ");
            scanf("%lf", &b);
            while (b==0)
            {
                printf("ERROR: No se puede dividir por 0, ingrese de vuelta: ");
                scanf("%lf",&b);
            }
            
            resultado = a / b;
            printf("El resultado de la division de %.2f / %.2f es %.2f\n",a,b, resultado);
            break;
        case '-':
            printf("La opreacion elegida fue RESTA\n");
            printf("Ingrese el primer numero: ");
            scanf("%lf", &a);
            printf("Ingrese el segundo: ");
            scanf("%lf", &b);
            resultado = a - b;
            printf("El resultado de la resta de %.2f - %.2f es %.2f\n",a,b, resultado);
            break;
        case '^':
            printf("La opreacion elegida fue POTENCIACION\n");
            printf("Ingrese la base: ");
            scanf("%lf", &a);
            printf("Ingrese el exponente: ");
            scanf("%lf", &b);
            resultado = pow(a,b);
            printf("El resultado de %.2f ^ %.2f es %.2f\n",a,b, resultado);
            break;

        default:
            break;
        }
    }

    return 0;
}