#include <Arduino.h>

void ejecutar_suma_enteros() {
    long iteraciones = 100000000;
    unsigned long tiempoInicio = millis();

    volatile int suma = 0;

    for(long i= 0;i<iteraciones; i++){
        suma +=1;
    }
    unsigned long tiempoFin = millis();
    Serial.printf("Prueba Enteros finalizada en: %lu ms\n", tiempoFin - tiempoInicio);
}

void ejecutar_suma_float() {
    long iteraciones = 100000000;
    unsigned long tiempoInicio = millis();

    volatile float suma = 0.0;

    for(long i= 0;i<iteraciones; i++){
        suma +=1.1f;
    }
    unsigned long tiempoFin = millis();
    Serial.printf("Prueba flotantes finalizada en: %lu ms\n", tiempoFin - tiempoInicio);
}

void setup(){
    Serial.begin(115200);
    delay(2000); // Espera 2000 ms

    Serial.println("Configurando CPU a 80 MHz");
    setCpuFrequencyMhz(80);
    ejecutar_suma_enteros();
    ejecutar_suma_float();

    Serial.println("Configurando CPU a 160 MHz");
    setCpuFrequencyMhz(160);
    ejecutar_suma_enteros();
    ejecutar_suma_float();
}

void loop(){}