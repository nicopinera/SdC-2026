# Trabajo práctico 2 - Stack frame

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

**Fecha:** 21/04/2026

---

## Información de los autores

- **Información de contacto**:
  - [nicolas.pinera@mi.unc.edu.ar](mailto:nicolas.pinera@mi.unc.edu.ar)
  - [julian.krede@mi.unc.edu.ar](mailto:julian.krede@mi.unc.edu.ar)
  - [juana.pucheta.noguera@mi.unc.edu.ar](mailto:juana.pucheta.noguera@mi.unc.edu.ar)

---

## Introducción

<!-- Aca podría explicarse brevemente que es el indice GINI y que se busca hacer con este tp a grandes rasgos-->

## Desarrollo

### Programa índice GINI: Arquitectura del sistema

En esta primera parte del trabajo se implementó un programa multilenguaje utilizando Python, C y ensamblador, con el objetivo de analizar cómo interactúan distintos niveles de abstracción dentro de un sistema, desde la lógica de aplicación hasta el estado directo del procesador.

Desde el punto de vista teórico, el sistema se apoya en la jerarquía de abstracción propia de la computación. Los lenguajes de alto nivel, como Python, priorizan la productividad y la facilidad de uso, ocultando detalles del hardware. En contraste, lenguajes de bajo nivel como el ensamblador operan prácticamente sin abstracciones, permitiendo un control explícito sobre registros, memoria e instrucciones de CPU. Entre ambos niveles, C actúa como un puente, ya que combina capacidades de alto nivel con acceso directo a memoria mediante punteros.

En base a esta idea, se diseñó una arquitectura de tres capas:

- Capa de orquestación (Python): Implementada en `src/main.py`, donde se gestiona la lógica principal del programa. Se utiliza la librería `requests` para obtener datos del índice GINI desde la API REST del Banco Mundial. Luego, mediante el módulo `ctypes`, se carga dinámicamente una biblioteca escrita en C. Una vez procesados los datos, se genera un archivo `.txt` que se utiliza en la segunda parte del trabajo y se grafica la evolución del índice a lo largo del tiempo.

- Capa de interfaz (C): Implementada en `src/libpython.c`. Su función es actuar como intermediario entre Python y el código en ensamblador. Aquí no se realiza procesamiento complejo, sino que simplemente se encapsula y expone la llamada a la subrutina en ASM, gestionando el paso de parámetros y el retorno de valores.

- Capa de optimización (Ensamblador): Implementada en `src/func_asm.asm` utilizando NASM. En esta capa se define una subrutina que recibe un valor de tipo `float`, lo trunca a `int`, le suma 1 y retorna el resultado. Esta operación se realiza directamente a nivel de instrucciones de CPU, sin abstracciones adicionales, evidenciando el control fino que ofrece este nivel.

De esta forma, el programa no solo cumple una función aplicada (procesar y visualizar el índice GINI), sino que también sirve como ejemplo concreto de cómo se articulan distintas capas de abstracción en un sistema real, mostrando el rol específico que cumple cada lenguaje dentro de la arquitectura.

#### Diferencia entre python y C

Python es un lenguaje cuya ejecución depende de un intérprete. A diferencia de C, el código fuente se traduce primero a un formato intermedio llamado Bytecode y luego es ejecutado por la Máquina Virtual de Python (PVM). Esto implica que el programa no corre de forma autónoma, sino que reside y es gestionado íntegramente dentro del entorno y el espacio de memoria del proceso python3.

C es un lenguaje de compilación nativa. El código fuente es compilado y se obtiene un archivo binario que contiene instrucciones en lenguaje máquina específicas para la arquitectura del procesador. Al ejecutarse, el procesador procesa estas instrucciones de forma directa y nativa, sin intermediarios, lo que permite un control total sobre el hardware y una velocidad de ejecución máxima.

#### Integración de las distintas capas

Para materializar la arquitectura propuesta, es necesario establecer un mecanismo de interoperabilidad entre la capa de orquestación (Python) y la capa de interfaz (C). Esta integración se logra mediante la compilación del código C como una librería dinámica (shared object) y su posterior carga en tiempo de ejecución desde Python utilizando el módulo `ctypes`.

El proceso se divide en dos etapas:

##### 1. Compilación del código C como librería dinámica

El código fuente en C se compila utilizando el compilador `gcc` con la opción `-shared`, lo que genera un archivo binario reutilizable. Este archivo contiene las funciones exportadas que actuarán como interfaz hacia niveles superiores.

Conceptualmente, este paso transforma el código C en un módulo binario independiente, accesible desde otros lenguajes. Es importante que las funciones expuestas respeten convenciones de llamada compatibles (en nuestro caso, System V AMD64 ABI), ya que Python interactuará con ellas a nivel de memoria y registros. En nuestro caso:

```bash
nasm -f elf64 -g src/func_asm.asm -o func_asm.o # Compila para obtener el codigo objeto del archivo en ASM
gcc -fPIC -c src/libpython.c -o libpython.o     # Compila para obtener el codigo objeto del archivo en C
gcc -shared func_asm.o libpython.o -o libpython.so # Se crea la libreria dinamica a partir del codigo objeto de los anteriores
```

##### 2. Carga y uso de la librería desde Python mediante `ctypes`

Una vez generada la librería dinámica, Python la carga en tiempo de ejecución utilizando `ctypes`. Este módulo permite invocar funciones escritas en C como si fueran funciones nativas de Python, pero operando directamente sobre memoria nativa. Por ejemplo para nuestro caso:

```python
import ctypes

# Obtiene la ruta a la libreria
ruta_lib = os.path.join(RUTA_BASE,"libpython.so")

# Carga la librería
lib = ctypes.CDLL(ruta_lib)

# Define el tipo del argumento de la funcion procesar_datos
lib.procesar_datos.argtypes = [ctypes.c_float]

# Define el tipo de retorno de la funcion procesar_datos
lib.procesar_datos.restype = ctypes.c_int
# Ahora se puede usar la funcion normalmente en cualquier parte haciendo lib.procesar_datos

# En nuestro caso lo usamos dentro de un for para obtener el indice de diferentes años consecutivos
for i in valores:
        r = lib.procesar_datos(ctypes.c_float(i))
        datos_casteados.append(r)

```

<!-- Aca podriamos meter una seccion que explique a grandes rasgos la convencion de llamada System V AMD64 ABI  -->

### Analisis de código en C con gdb

Para realizar un análisis del funcionamiento del stack frame implementamos una programa en C que lee los datos recogidos por el programa en python (a través de un archivo `.txt`) y los imprime por pantalla, dentro de este programa implementamos una función que se encarga de realizar el casteo del valor en flotante a entero y sumarle 1. Para analizar la ejecución del programa utilizamos gdb dashboard:

![interfaz gdb dashboard](https://github.com/user-attachments/assets/7f23b7ab-42fd-4bbd-9ebf-80c0544ec043)

Como se puede observar en la parte superior tenemos las instrucciones correspondientes en ensamblador a de la instrucción en C actual, ademas se puede observar el código en C correspondiente en el apartado *Source* y el estado actual de los registros en el apartado *Registers*. Ademas:

- En *Source* La línea en verde es la próxima linea en C a ejecutar (lo que GDB llama current execution line). Es a donde apunta el RIP en ese momento. 
- A su vez en la parte superior se remarca con verde las instrucciones en ensamblador a la que corresponde dicha linea de C. 
- Los registros en verde indican valores que cambiaron respecto de la instrucción anterior.

Para avanzar en gdb hay 3 comandos útiles:

`step` (`s`): Avanza a la siguiente línea de código fuente, entrando en funciones si corresponde.
`next` (`n`): Avanza a la siguiente línea de código fuente sin entrar en funciones.
`stepi` (`si`): Avanza una instrucción de ensamblador.

Avanzando hasta la parte que nos interesa que es la llamada a una función, en nuestro caso `castear_datos`:

![Antes de entrar a la función](https://github.com/user-attachments/assets/7f23b7ab-42fd-4bbd-9ebf-80c0544ec043)

Como se puede observar antes de entrar a la función, se mueve el valor del parametro (que esta almacenado como variable local de la función main) al registro `xmm0`, siguiendo la convención System V AMD64 ABI, posteriormente entra a la función mediante la instrucción `call` indicando la dirección en memoria de la función `castear_datos`.

![Dentro de la función](https://github.com/user-attachments/assets/deca00e1-2338-4393-aef4-1fb6c165ccd9)

Al entrar en la función vemos el prologo de la función, guarda el `rbp` de la función anterior (`main`) en el stack y luego carga el valor del `rbp` de la función actual copiando el valor del stack pointer (`rsp`), de esta manera se establece un nuevo stack frame.

![Guardado de ebp actual](https://github.com/user-attachments/assets/5af0f1d2-aa79-4445-bb40-e5350daeb2d2)

Luego se ve cómo se almacena el valor del parámetro x, que fue pasado en el registro xmm0, dentro del stack frame de la función actual mediante la instrucción `movss`, esto no es estrictamente necesario desde el punto de vista funcional, ya que el valor ya se encuentra disponible en un registro, pero en compilaciones sin optimización (`-O0`).

Después de haber guardado `x` en el stack, se carga nuevamente el valor en `xmm0`, esto es redundante, sucede porque el compilador fuerza el uso de memoria para mantener consistencia con el modelo de variables.

Luego se trunca el valor almacenado en `xmm0` y se almacena en `eax`, esto se hace mediante la instrucción `cvttss2si` y luego se le suma 1 mediante la instrucción `add`. Se almacena el valor y luego es guardado en el `eax`, ya que en este registro se almacena el valor de retorno.

Posteriormente se ejecuta el epilogo de la función que consiste en recuperar el valor de `rbp` almacenado anteriormente, esto se realiza mediante la instrucción `pop` y finalmente se retorna de la función con `ret`

![Retorno de la función](https://github.com/user-attachments/assets/d922215c-0d84-4a0c-b058-1a5928c49781)

---

## Referencias

- [System V ABI](https://wiki.osdev.org/System_V_ABI)