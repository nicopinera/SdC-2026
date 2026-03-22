# Trabajo practico 1 - Rendimiento

## Nombres

- Nicolas Piñera
- Julian Krede
- Juana Pucheta

**Nombre del grupo**: Bare metal guys

## UNC - Facultad de Ciencias Exactas, Físicas y Naturales

## Cátedra: Sistema de Computadoras

### Profesores

- Javier Alejandro JORGE

- Solinas, Miguel Ángel

**Fecha:** 21/3/2026

---

## Información de los autores

- **Información de contacto**:
  - [nicolas.pinera@mi.unc.edu.ar](mailto:nicolas.pinera@mi.unc.edu.ar)
  - [julian.krede@mi.unc.edu.ar](mailto:julian.krede@mi.unc.edu.ar)

---

## Resumen

**Palabras clave**:

---

## Introducción

---

## Resultados

### Práctica: Rendimiento ESP32

Para esta primera práctica, se realizó un código en C++ para la ESP32 en el cual se modifica la frecuencia del procesador, primero a **80 MHz** y luego a **160 MHz**. Se ejecuta un bucle `for` donde se realizan sumas de enteros y números flotantes. Posteriormente, se obtienen los tiempos que demora cada proceso de suma con cada una de las frecuencias. El código se encuentra en el siguiente enlace: [Código ESP32](/TP1/ESP32/src/main.cpp)

```bash
CPU a 80 MHz
Prueba Enteros finalizada en: 14204 ms
Prueba flotantes finalizada en: 16787 ms
Configurando CPU a 160 MHz
Prueba Enteros finalizada en: 6987 ms
Prueba flotantes finalizada en: 8257 ms
```

Utilizando la siguiente formula de Speedup se puede obtener los siguientes resultados:

$$ Speedup = \frac{RedimientoMejorado}{RednimientoOriginal} = \frac{EX*{Original}}{EX*{Mejorado}} $$

Siendo $EX$ el tiempo de ejecucion de la CPU.

| Frecuencia (MHz) | Tiempo Enteros (s) | Tiempo Floats (s) | Speedup (vs la base) |
| ---------------- | ------------------ | ----------------- | -------------------- |
| 80               | 14.2               | 16.7              | 1                    |
| 160              | 6.9                | 8.2               | 2.033                |

En función de estos resultados, se observa que el tiempo de ejecución se ha reducido 2.033 veces en ambos casos. El tiempo es una medida real del rendimiento: si el tiempo disminuye al aumentar la frecuencia, el rendimiento aumenta. Además, se nota que el procesador no tiene el mismo rendimiento (a la misma frecuencia) para operaciones de números enteros que para flotantes; esto se debe a que las operaciones de punto flotante suelen tener un CPI (Ciclos por Instrucción) más alto, ya que requieren más microinstrucciones para completarse.

### Benchmark para tareas diarias

En funcion de lo visto en clases, sabemos que un benchmark son programas de prueba que se utilizan para medir el rendimiendo del hardware en situaciones especificas. En funcion de esto y lo analizado con el grupo se eligieron los siguientes benchmarks mas utiles para nosotros y que nos sirven para analizar el rendimiento:

| Tarea                   | Benchmark                                                                                                                                |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Jugar                   | **3DMark Time Spy** ( Rendimiento grafico) y algunos video juegos traen un benchmark integrado para probar el rendimiento del procesador |
| Ofimatica               | **PCMark 10** para trabajo con office y **Benchmarks de Navegador** para web                                                             |
| Programacion            | **Timed Linux Kernel Compilation**                                                                                                       |
| Simulación de Circuitos | **Phoronix Test Suite**, utiliza Ngspice para simular circuitos                                                                          |
| Compilación de Firmware | **CoreMark**                                                                                                                             |

### Comparativa de Procesadores

A continuacion se realiza la comparativa de rendimiento para compilar el kernel de linux para los siguientes procesadores:

- Intel Core i5-13600K (Sera nuestra base para comparar)
- AMD Ryzen 9 5900X 12-Core
- AMD Ryzen 9 7950X 16-Core

> Cuanto tiempo demoran cada uno
> Cual de ellos hace un uso mas eficiente de los nucleos que tiene
> Cual es mas eficiente en terminos de costo (dividir el tiempo que se demora por el costo y el tiempo por la cantida de procesadores) costo energetico y monetario

### Analisis de rendimiento de Codigo - Profiling

El profiling es una tecnica de analisis que mide el tiempo de ejecucion o el uso de memoria/recursos mientras de ejecuta, ademas nos permite ver cuanto tiempo tarda en ejecutarse cada funcion o metodo.

> Realizar Analisis en funcion de la herramienta gprof

---

## Conclusiones

## Referencias
