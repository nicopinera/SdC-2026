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

$$ Speedup = \frac{RedimientoMejorado}{RednimientoOriginal} = \frac{EX_{Original}}{EX_{Mejorado}} $$

Siendo $EX$ el tiempo de ejecucion de la CPU.

| Frecuencia (MHz) | Tiempo Enteros (s) | Tiempo Floats (s) | Speedup (vs la base) |
| ---------------- | ------------------ | ----------------- | -------------------- |
| 80               | 14.2               | 16.7              | 1                    |
| 160              | 6.9                | 8.2               | 2.033                |

En función de estos resultados, se observa que el tiempo de ejecución se ha reducido 2.033 veces en ambos casos. El tiempo es una medida real del rendimiento: si el tiempo disminuye al aumentar la frecuencia, el rendimiento aumenta. Además, se nota que el procesador no tiene el mismo rendimiento (a la misma frecuencia) para operaciones de números enteros que para flotantes; esto se debe a que las operaciones de punto flotante suelen tener un CPI (Ciclos por Instrucción) más alto, ya que requieren más microinstrucciones para completarse.

---

## Conclusiones

## Referencias
