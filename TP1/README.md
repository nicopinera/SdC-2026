# Trabajo práctico 1 - Rendimiento

## Nombres

- Nicolás Piñera
- Julián Krede
- Juana Pucheta Noguera

**Nombre del grupo**: Bare metal guys

## UNC - Facultad de Ciencias Exactas, Físicas y Naturales

## Cátedra: Sistema de Computadoras

### Profesores

- Javier Alejandro Jorge
- Miguel Ángel Solinas

**Fecha:** 21/3/2026

---

## Información de los autores

- **Información de contacto**:
  - [nicolas.pinera@mi.unc.edu.ar](mailto:nicolas.pinera@mi.unc.edu.ar)
  - [julian.krede@mi.unc.edu.ar](mailto:julian.krede@mi.unc.edu.ar)
  - [juana.pucheta.noguera@mi.unc.edu.ar](mailto:juana.pucheta.noguera@mi.unc.edu.ar)

---

## Introducción

El presente trabajo práctico tiene como objetivo el estudio y análisis del rendimiento (performance) en sistemas de computación, abordando tanto plataformas embebidas como procesadores de propósito general. El rendimiento no es una métrica unidimensional; depende de una compleja interacción entre la frecuencia del reloj, la arquitectura del conjunto de instrucciones (ISA), la eficiencia del compilador y la naturaleza de la carga de trabajo.

A lo largo del informe, se exploran tres ejes fundamentales:

- **Análisis de Hardware Embebido**: Se evalúa el impacto de la frecuencia de reloj en una plataforma ESP32, cuantificando la mejora mediante la métrica de Speedup y diferenciando el costo computacional entre operaciones de enteros y punto flotante.

- **Benchmarking y Comparativa de Mercado**: Se analizan procesadores de consumo masivo (Intel Core i5 vs. AMD Ryzen 9) bajo cargas de trabajo reales (compilación del Kernel de Linux), introduciendo métricas críticas para la toma de decisiones como el rendimiento por vatio (eficiencia energética) y el rendimiento por dólar (costo-beneficio).

- **Análisis Dinámico de Software (Profiling)**: Se profundiza en el uso de herramientas de diagnóstico como gprof (instrumentación) y perf (muestreo) para identificar "cuellos de botella" en el código fuente, permitiendo una optimización basada en datos reales de ejecución.

Mediante este enfoque integral, se busca comprender cómo los recursos de hardware son utilizados por el software y cómo las limitaciones físicas del procesador condicionan el tiempo de ejecución final de una tarea.

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

Utilizando la siguiente fórmula de Speedup se pueden obtener los siguientes resultados:

$$ Speedup = \frac{RendimientoMejorado}{RendimientoOriginal} = \frac{EX*{Original}}{EX*{Mejorado}} $$

Siendo $EX$ el tiempo de ejecución de la CPU.

| Frecuencia (MHz) | Tiempo Enteros (s) | Tiempo Floats (s) | Speedup (vs la base) |
| ---------------- | ------------------ | ----------------- | -------------------- |
| 80               | 14.2               | 16.7              | 1                    |
| 160              | 6.9                | 8.2               | 2.033                |

En función de estos resultados, se observa que el tiempo de ejecución se ha reducido 2.033 veces en ambos casos. El tiempo es una medida real del rendimiento: si el tiempo disminuye al aumentar la frecuencia, el rendimiento aumenta. Además, se nota que el procesador no tiene el mismo rendimiento (a la misma frecuencia) para operaciones de números enteros que para flotantes; esto se debe a que las operaciones de punto flotante suelen tener un CPI (Ciclos por Instrucción) más alto, ya que requieren más microinstrucciones para completarse.

### Benchmark para tareas diarias

En función de lo visto en clases, sabemos que un benchmark son programas de prueba que se utilizan para medir el rendimiento del hardware en situaciones específicas. En función de esto y lo analizado con el grupo, se eligieron los siguientes benchmarks más útiles para nosotros y que nos sirven para analizar el rendimiento:

| Tarea                   | Benchmark                                                                                                                              |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Jugar                   | **3DMark Time Spy** (Rendimiento gráfico) y algunos videojuegos traen un benchmark integrado para probar el rendimiento del procesador |
| Ofimática               | **PCMark 10** para trabajo con office y **Benchmarks de Navegador** para web                                                           |
| Programación            | **Timed Linux Kernel Compilation**                                                                                                     |
| Simulación de Circuitos | **Phoronix Test Suite**, utiliza Ngspice para simular circuitos                                                                        |
| Compilación de Firmware | **CoreMark**                                                                                                                           |

### Comparativa de Procesadores

A continuación, se realiza la comparativa de rendimiento para **compilar el kernel de Linux** para los siguientes procesadores:

- **Intel Core i5-13600K**: Será nuestra base para comparar. Posee 14 núcleos y 20 hilos con una frecuencia de 5.1 GHz.
- **AMD Ryzen 9 5900X 12-Core**: 12 núcleos y 24 hilos a 3.7 GHz.
- **AMD Ryzen 9 7950X 16-Core**: 16 núcleos y 32 hilos a 4.5 GHz.

| Procesador           | Tiempo promedio en compilar (s) |
| -------------------- | ------------------------------- |
| Intel Core i5-13600K | 83                              |
| AMD Ryzen 9 5900X    | 97                              |
| AMD Ryzen 9 7950X    | 52                              |

Vemos que el procesador más rápido es el Ryzen 9 7950X y el más lento es el AMD Ryzen 9 5900X. Lo sorprendente es que el Intel es más rápido que el Ryzen 9 5900X, siendo este último una gama relativamente nueva en comparación con el Intel.

En función de esta información, calcularemos el rendimiento de cada uno con la siguiente fórmula: $Rendimiento = \frac{1}{EX_{CPU}}$, recordando que $EX_{CPU}$ es el tiempo de ejecución del CPU, en este caso, para compilar el kernel de Linux.

Luego, en función de la cantidad de núcleos que tiene el procesador, se calculará el rendimiento por núcleo utilizando la siguiente ecuación: $R_{núcleo} = \frac{Speedup}{N_{núcleos}}$.

| Procesador           | Número de núcleos | Rendimiento | Speedup | Speedup % | Eficiencia por núcleo |
| -------------------- | ----------------- | ----------- | ------- | --------- | --------------------- |
| Intel Core i5-13600K | 14                | 0.012       | 1       | 100%      | 0.07143 - 7.14%       |
| AMD Ryzen 9 5900X    | 12                | 0.0103      | 0.855   | 85.56%    | 0.0713 - 7.13%        |
| AMD Ryzen 9 7950X    | 16                | 0.019       | 1.595   | 159.5%    | 0.0974 - 9.974%       |

Vemos que el **rendimiento** es inversamente proporcional al tiempo de ejecución de esa tarea específica; además, es una medida absoluta de su capacidad. Si dividimos el rendimiento por el número de núcleos obtenemos la _capacidad absoluta por núcleo_, un número decimal muy pequeño y difícil de analizar.

Para realizar un mejor análisis del rendimiento es utilizar el **Speedup** o aceleración, que es una medida relativa de la mejora. Se toma como base el primer procesador, por eso su speedup es de 1 (o 100%). Al dividir este valor por la cantidad de recursos se obtiene la **Eficiencia**, que nos marca qué porcentaje del potencial teórico de cada recurso, en este caso núcleos, se está aprovechando realmente en comparación con una base de referencia.

En el uso de los procesadores o núcleos, el Intel es nuestra base de referencia. El procesador ganador es el Ryzen 9 7950X ya que no solo es más rápido por tener más núcleos, sino que su arquitectura aprovecha mejor cada unidad de procesamiento disponible en comparación con los otros dos.

Para obtener un análisis extra, veremos el rendimiento por dólar y el rendimiento por vatio, dividiendo el rendimiento del procesador por el precio y el rendimiento por el consumo en vatios.

| Procesador           | Número de núcleos | Rendimiento | Precio [Dólar] | Consumo [W] | Rendimiento por Dólar | Rendimiento por W |
| -------------------- | ----------------- | ----------- | -------------- | ----------- | --------------------- | ----------------- |
| Intel Core i5-13600K | 14                | 0.012       | 319            | 125         | 3.76e-5               | 9.6e-5            |
| AMD Ryzen 9 5900X    | 12                | 0.0103      | 255            | 105         | 4.039e-5              | 9.8e-5            |
| AMD Ryzen 9 7950X    | 16                | 0.019       | 699            | 170         | 2.75e-5               | 11.3e-5           |

Al comparar los procesadores usando la métrica de rendimiento por dólar (definida como el rendimiento dividido por el costo), se observa que el AMD Ryzen 9 5900X presenta el valor más alto. Esto implica que es el que ofrece mayor rendimiento por unidad de costo, por lo que resulta ser la mejor opción según esta métrica.

Por otro lado, al comparar los procesadores utilizando la métrica de rendimiento por vatio (rendimiento dividido por el consumo de potencia), el AMD Ryzen 9 7950X presenta el mayor valor, lo que indica que es el más eficiente desde el punto de vista energético.

### Análisis de rendimiento de código - Profiling

El profiling es una técnica de análisis que mide el comportamiento de un programa durante su ejecución, recolectando métricas como tiempo de ejecución, uso de memoria y otros recursos. Además, permite descomponer ese comportamiento para identificar cuánto tiempo o recursos consume cada función o método.

#### Analisis utilizando gprof

gprof es una herramienta de profiling para programas C/C++ que funciona por instrumentación: al compilar con el flag `-pg`, el compilador inserta código extra en cada función para registrar cuántas veces fue llamada y cuánto tiempo consumió. Al ejecutar el programa, se genera un archivo `gmon.out` que gprof analiza para producir un reporte con el call graph y el flat profile. Este enfoque ofrece datos exactos de conteo de llamadas, a costa de mayor overhead en tiempo de ejecución y la necesidad de recompilar el binario.

Al ejecutar gprof se obtiene la salida volcada en el siguiente archivo:

[Resultado gprof](/TP1/data/analisis.txt)

En el archivo generado se distinguen dos principales secciones:

- **Flat Profile**: Evidencia el tiempo total usado en cada función en forma individual. Particularmente en nuestro caso, las funciones `func2`, `func1` y `new_func1` se reparten casi equitativamente el tiempo de ejecución (aproximadamente 33% cada una), tardando unos 10 segundos cada una. Esto indica que el programa tiene una carga de trabajo distribuida simétricamente entre ellas.

- **Call Graph**: Muestra la jerarquía de quién llama a quién. Podemos observar que `main` llama a `func1` y `func2` y, a su vez, `func1` es quien llama a `new_func1`. Esto explica por qué en el "Call Graph", `func1` aparece con un tiempo total del 65.6% (su tiempo propio más el de a quien llamó, `new_func1`).

#### Análisis utilizando Perf

`perf` es una herramienta de profiling de Linux basada en muestreo, que utiliza contadores de hardware del CPU para estimar en qué partes del código se consume el tiempo de ejecución. Este enfoque introduce menor overhead, a costa de ser menos preciso que el profiling por instrumentación.

Al ejecutar Perf se obtiene la siguiente salida:

![Resultado perf](https://github.com/user-attachments/assets/1df76a72-d41c-4c58-be23-ae7becdcb162)

Esto indica que **aproximadamente** del total de tiempo de ejecución:

- La función `func2` se ejecuta el 33.79% del tiempo.
- La función `new_func1` se ejecuta el 33.63% del tiempo.
- La función `func1` se ejecuta el 31.79% del tiempo.
- La función `main` se ejecuta el 0.13% del tiempo.

Observando más en detalle las instrucciones de las funciones

- Instrucciones ejecutadas en `func1`

![Resultado func1](https://github.com/user-attachments/assets/17ef95fa-8cc6-46b6-9582-7795ccf8ee9a)

- Instrucciones ejecutadas en `new_func1`

![Resultado new_func1](https://github.com/user-attachments/assets/d7e8f1f1-3a33-41f3-8e37-9db1bf7e8d51)

- Instrucciones ejecutadas en `func2`

![Resultado func2](https://github.com/user-attachments/assets/1c39629f-98a4-4850-8636-9fe9fec81042)

Las tres funciones tienen el mismo patrón fundamental: un loop con dependencia fuerte en el contador.

**Diferencias**:

- `func1`: Usa memoria directamente en `cmp`.
- `func2` y `new_func1`: Usan un registro intermedio.

Pero estas diferencias no cambian significativamente el costo total, porque el problema real es la dependencia secuencial del loop.

---

## Referencias

- [GPROF y Perf](https://docs.google.com/document/d/1lj3KkO_GthTn3WyfkUsLMWJvGdXblKGyIsxCLVGQOZg/edit?tab=t.0)
- [Tiempo para compilar el Kernel de Linux](https://openbenchmarking.org/test/pts/build-linux-kernel&eval=a94fc255324a86f95ba5207758d45b3e012d6e50#metrics)
- [Cálculos realizados sobre rendimiento](/TP1/src/main.py)
- [Perf](https://dev.to/etcwilde/perf---perfect-profiling-of-cc-on-linux-of)
