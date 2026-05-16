# Trabajo práctico 4 - Modulos de Kernel

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

**Fecha:** 4/5/2026

---

## Información de los autores

- **Información de contacto**:
  - [nicolas.pinera@mi.unc.edu.ar](mailto:nicolas.pinera@mi.unc.edu.ar)
  - [julian.krede@mi.unc.edu.ar](mailto:julian.krede@mi.unc.edu.ar)
  - [juana.pucheta.noguera@mi.unc.edu.ar](mailto:juana.pucheta.noguera@mi.unc.edu.ar)

---

## Introducción

## Resultados

### CheckInstall

CheckInstall es una herramienta de administración de software para sistemas operativos basados en Unix/Linux que automatiza la creación de paquetes binarios a partir de código fuente. Su función principal es interceptar el proceso de instalación manual para generar un paquete manejable por el gestor de paquetes local (como APT, RPM o Pacman).

En el flujo de trabajo estándar de compilación, el comando final distribuye archivos a través de diversos directorios del sistema de archivos sin que el gestor de paquetes tenga registro de ellos. Esto dificulta la actualización, el rastreo y, especialmente, la desinstalación limpia del software. CheckInstall interviene en este proceso mediante las siguientes acciones:

1. **Monitorización de archivos**: Realiza un seguimiento de cada archivo que el script de instalación intenta crear o modificar en el sistema.
2. **Encapsulamiento**: En lugar de permitir una instalación dispersa, agrupa todos los archivos resultantes en un único paquete binario (por ejemplo, un archivo *.deb* para Debian/Ubuntu o *.rpm* para Red Hat/Fedora).
3. **Integración con el Gestor de Paquetes**: Instala dicho paquete utilizando las utilidades del sistema, asegurando que el software figure en la base de datos de aplicaciones instaladas.

Es importante notar que CheckInstall está diseñado para la gestión de sistemas locales o entornos de pruebas. No genera paquetes que cumplan estrictamente con las políticas de empaquetado de las distribuciones (como las Debian Policy Manual), por lo que no debe sustituir a las herramientas de empaquetado profesional si el objetivo es la distribución en repositorios públicos oficiales.

#### Creacion de un paquete para Ubuntu con CheckInstall

Para esta seccion decidimos crear un pequeño paquete, en vez del hola mundo tradicional, creamos una calculadora con operaciones basicas (multiplicacion,division,suma,resta y potencia), se puede encontrar el codigo fuente en [Calculadora](/TP4/src/paquete/main.c). Para que el proceso de empaquetamiento sea exitoso, el sistema debe contar con el conjunto de herramientas de desarrollo estándar:

- build-essential: Contiene el compilador gcc y la utilidad make. Son necesarios para transformar el código fuente en un binario ejecutable.
- checkinstall: La herramienta núcleo que monitorea la instalación y genera el paquete .deb, .rpm o Slackware.
- Archivos de Proyecto:
  - Código Fuente (.c): El programa en lenguaje de alto nivel.
  - Makefile: El archivo de configuración que define las instrucciones de compilación e instalación. Es el que permite a checkinstall automatizar el proceso.

El Makefile es la pieza fundamental porque actúa como el "mapa" para checkinstall. Sin un bloque de instrucción install, la herramienta no sabrá qué archivos debe incluir en el paquete. Una consideracion importante es el uso de la variable $(DESTDIR) en entornos de empaquetado, ya que permite redirigir la instalación a una ubicación temporal durante la creación del paquete sin afectar los directorios raíz del sistema prematuramente.

Una vez tenemos todo ejecutamos lo siguiente:

```bash
# Compilamos el codigo
make

# Generamos el paquete
sudo checkinstall
```

En lugar de utilizar `sudo make install`, se invoca a **checkinstall**. Esta herramienta ejecutará las instrucciones de instalación del Makefile dentro de un entorno controlado. Durante la ejecución, el administrador debe interactuar con la terminal para definir la identidad del paquete: Descripción, Nombre del paquete y  Versión y Arquitectura.

![Ejecion del paquete instalado](https://github.com/user-attachments/assets/865416ea-6d9e-4003-8e93-8f9108d58856)

### Funciones de un programa vs un modulo

La disponibilidad de funciones y la forma en que estas se invocan dependen estrictamente del nivel de privilegio en el que se ejecuta el código. Esta distinción es fundamental para la estabilidad y seguridad del sistema operativo.

#### Programa

Un programa convencional opera en el **modo usuario** y sus capacidades están limitadas por el entorno de ejecución proporcionado por las bibliotecas del sistema.

- **Punto de Entrada**: Utiliza la función estándar **main()** como inicio de la ejecución.
- **Bibliotecas Estándar (API)**: Tiene acceso a funciones de alto nivel proporcionadas por bibliotecas como glibc (printf(), malloc(), scanf()).
- **Llamadas al Sistema (Syscalls)**: Para interactuar con el hardware o realizar tareas protegidas (leer un archivo, enviar datos por red), el programa debe invocar funciones de interfaz que solicitan permiso al kernel (ej. read(), write(), open()).
- **Aislamiento**: Las funciones de un programa no pueden acceder directamente a la memoria de otro programa ni a las estructuras internas del núcleo.

#### Modulo

Un **módulo cargable del núcleo (LKM)** se ejecuta en el **modo supervisor o espacio de kernel**, formando parte del corazón del sistema operativo.

- **Punto de Entrada y Salida**: No posee un main(). En su lugar, implementa funciones de registro y desregistro, típicamente module_init() (para inicializar recursos) y module_exit() (para liberarlos).
- **Funciones del Núcleo (Símbolos Exportados)**: No puede utilizar bibliotecas de usuario (no existe stdio.h en el kernel). Utiliza funciones internas del núcleo que han sido "exportadas" para ser compartidas. Por ejemplo: printk() (equivalente a printf para el log del sistema) o kmalloc() (para gestión de memoria física).
- **Gestión de Interrupciones y Drivers**: Tiene acceso a funciones de bajo nivel para manipular registros de hardware, gestionar interrupciones (IRQs) y registrarse como manejador de dispositivos (drivers).
- **Privilegio Total**: Las funciones de un módulo pueden acceder a cualquier dirección de memoria del sistema, lo que otorga máxima potencia pero conlleva el riesgo de que un error de programación detenga el sistema completo (Kernel Panic).

### Espacio de Usuario vs Kernel

El procesador utiliza mecanismos de protección (niveles de privilegio o rings) para separar estas dos áreas de memoria RAM para proteger la estabilidad del equipo:

- **Espacio de Usuario (User Space)**: Es el área de memoria donde se ejecutan las aplicaciones del usuario. Las aplicaciones aquí tienen un privilegio restringido; no pueden acceder directamente al hardware ni a la memoria de otros procesos. Si un programa falla, el sistema operativo permanece estable.
- **Espacio del Kernel (Kernel Space)**: Es el área donde reside el núcleo del sistema operativo y sus extensiones (módulos). Tiene acceso total y sin restricciones al hardware y a toda la memoria del sistema. Un error en este espacio puede provocar un fallo crítico del sistema (Kernel Panic).

### Espacio de datos

En el contexto de la ejecución de procesos, el espacio de datos es la sección de la memoria virtual asignada a un programa que contiene las variables y estructuras necesarias para su funcionamiento. Se subdivide principalmente en:

- **Datos estáticos**: Variables globales y estáticas inicializadas durante la compilación.
- **Heap (Montículo):** Memoria dinámica solicitada en tiempo de ejecución (ej. mediante malloc).
- **Stack (Pila):** Almacena variables locales y direcciones de retorno de funciones.

En el desarrollo de módulos, el espacio de datos es crítico, ya que el kernel debe gestionar su propia memoria de forma manual y extremadamente cuidadosa para evitar fugas de memoria (memory leaks) que comprometan la estabilidad global.

### Drivers y /dev

Los drivers (controladores de dispositivos) actúan como traductores entre el sistema operativo y el hardware físico. En sistemas tipo Unix, se implementa la filosofía de que "todo es un archivo", lo que permite interactuar con el hardware a través del sistema de archivos.

El directorio /dev (devices) contiene archivos especiales que representan los dispositivos del sistema. No son archivos almacenados en el disco, sino interfaces para comunicarse con los drivers del kernel.
