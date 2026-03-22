# Trabajo practico 1 - Rendimiento

## Nombres

- Nicolas Piñera
- Julian Krede
- Juana Pucheta Noguera

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
  - [juana.pucheta.noguera@mi.unc.edu.ar](mailto:juana.pucheta.noguera@mi.unc.edu.ar)

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

$$ Speedup = \frac{RedimientoMejorado}{RednimientoOriginal} = \frac{EX_{Original}}{EX_{Mejorado}} $$

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

A continuacion se realiza la comparativa de rendimiento para **compilar el kernel de linux** para los siguientes procesadores:

- **Intel Core i5-13600K**: Sera nuestra base para comparar. Posee 14 cores y 20 thread con una frecuencia de 5.1 GHz.
- **AMD Ryzen 9 5900X 12-Core**: 12 cores y 24 threads a 3.7 GHz
- **AMD Ryzen 9 7950X 16-Core**: 16 Cores y 32 threads a 4.5 GHz

| Procesador           | Tiempo promedio en compilar (s) |
| -------------------- | ------------------------------- |
| Intel Core i5-13600K | 83                              |
| AMD Ryzen 9 5900X    | 97                              |
| AMD Ryzen 9 7950X    | 52                              |

Vemos que el procesador mas rapido es el Ryzen 9 7950X y el mas lento es el AMD Ryzen 9 5900X. Lo sorprendente es que el Intel es mas rapido que el Ryzen 9 5900X, siendo este ultimo una gama relativamente nueva en comparacion con el Intel.

En funcion de esta informacion calcularemos el rendimiento de cada uno con la siguiente formula: $Rendimiento = \frac{1}{EX_{CPU}}$ recordando que $EX_{CPU}$ es el tiempo de ejecucion del CPU, en este caso, para compilar el kernel de linux.

Luego, en funcion de la cantidad de nucleos que tiene el procesador, se calculara el rendimineto por nucleo utilizando la siguiente ecuacion $R_{nucleo} = \frac{Speedup}{N_{nucleos}}$

| Procesador           | Numero de nucleos | Rendimiento | Speedup | Speedup % | Eficiencia por nucleo |
| -------------------- | ----------------- | ----------- | ------- | --------- | --------------------- |
| Intel Core i5-13600K | 14                | 0.012       | 1       | 100%      | 0.07143 - 7.14%       |
| AMD Ryzen 9 5900X    | 12                | 0.0103      | 0.855   | 85.56%    | 0.0713 - 7.13%        |
| AMD Ryzen 9 7950X    | 16                | 0.019       | 1.595   | 159.5%    | 0.0974 - 9.974%       |

Vemos que el **rendimiento** es inversamente proporcional al tiempo de ejecucion de esa tarea especifica, ademas es una medida absoluta de su capacidad. Si dividimos el rendimiento por el numero de nucleos obtenemos la _capacidad absoluta por nucleo_, es un numero decimal muy pequeño y dificil de analisar.

Para realizar un mejor analisis del rendimiento es utilizar el **Speedup** o aceleracion que es una medida relativa de la mejora. Se toma como base el primer procesador, por eso su speedup es de 1 (o 100%). Al dividir este valor por la cantidad de recursos se obtiene la **Eficiencia**, que nos marca que porcentaje del potencial teorico de cada recurso, en este caso nucleos, se esta aprovechando realmente en comparacion con una base de referencia.

En el uso de los procesadores o nucleos, el Intel es nuestra base de referencia. El procesador ganador es el Ryzen 9 7950X ya que no solo es mas rapido por tener mas nucleos, sino que su arqutectura aprovecha mejor cada unidad de procesamiento disponible en comparacion de los otros dos.

Para obtener un analisis extra, veremos el rendimiento por dolar y el rendimiento por watts, dividiendo el rendimiento del procesador por el precio y el rendimiento por el consumo en watts.

| Procesador           | Numero de nucleos | Rendimiento | Precio [Dolar] | Consumo [W] | Rendimiento por Dolar | Rendimiento por W |
| -------------------- | ----------------- | ----------- | -------------- | ----------- | --------------------- | ----------------- |
| Intel Core i5-13600K | 14                | 0.012       | 319            | 125         | 3.76e-5               | 9.6e-5            |
| AMD Ryzen 9 5900X    | 12                | 0.0103      | 255            | 105         | 4.039e-5              | 9.8e-5            |
| AMD Ryzen 9 7950X    | 16                | 0.019       | 699            | 170         | 2.75e-5               | 0.000113          |

> Cuanto tiempo demoran cada uno
> Cual de ellos hace un uso mas eficiente de los nucleos que tiene
> Cual es mas eficiente en terminos de costo (dividir el tiempo que se demora por el costo y el tiempo por la cantida de procesadores) costo energetico y monetario

### Analisis de rendimiento de Codigo - Profiling

El profiling es una tecnica de analisis que mide el tiempo de ejecucion o el uso de memoria/recursos mientras de ejecuta, ademas nos permite ver cuanto tiempo tarda en ejecutarse cada funcion o metodo.

> Realizar Analisis en funcion de la herramienta gprof

---

## Referencias

- [GPROF y Perf](https://docs.google.com/document/d/1lj3KkO_GthTn3WyfkUsLMWJvGdXblKGyIsxCLVGQOZg/edit?tab=t.0)
- [Tiempo para compilar el Kernel de linux](https://openbenchmarking.org/test/pts/build-linux-kernel&eval=a94fc255324a86f95ba5207758d45b3e012d6e50#metrics)
