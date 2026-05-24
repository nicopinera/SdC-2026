# Trabajo práctico 3-B - UEFI

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

Sabemos que el proceso de arranque de una computadora es un entorno completo y sofisticado que gestiona el hardware, verifica la integridad del sistema y decide qué cargar: el firmware.

Durante mucho tiempo, este rol fue cumplido por el BIOS (Basic Input/Output System), un estándar desarrollado en los años 70 que, si bien fue revolucionario en su época, comenzó a mostrar limitaciones severas: soporte máximo de discos de 2TB, arranque en modo de 16 bits, interfaz rudimentaria y escasa capacidad de extensión.Para superar estas limitaciones, Intel desarrolló la especificación EFI (Extensible Firmware Interface), que luego evolucionó en el estándar abierto UEFI (Unified Extensible Firmware Interface), gestionado por el UEFI Forum con participación de los principales fabricantes de hardware y software del mundo.

Este trabajo práctico tiene como objetivo explorar este entorno desde una perspectiva técnica y práctica. Se desarrolla una aplicación nativa en C para UEFI que se ejecut en un entorno emulado con QEMU/OVMF y en hardware físico real (bare metal). A lo largo del trabajo se abordarán también conceptos de seguridad relevantes, como las técnicas de anti-debugging basadas en la detección del byte 0xCC (INT 3), que ilustran cómo el entorno pre-OS puede ser tanto un vector de ataque como un campo de análisis para la seguridad informática.

## Marco teórico

El proceso de inicialización de UEFI se enmarca dentro de la especificación PI (Platform Initialization), que define las etapas secuenciales por las cuales el firmware inicializa progresivamente el hardware antes de transferir el control al cargador del sistema operativo. Este proceso expone dos categorías de servicios fundamentales: los Boot Services, y los Runtime Services. Siendo los Boots Service aquellos disponible únicamente durante el arranque. Entre sus funciones principales se encuentran: Gestión de memoria, gestión de handles y protocolos, gestión de drivers e imágenes y eventos y temporizadores.
Por otro lado los Runtime service son servicios que persisten luego de que el SO tome el control, incluso una vez que los Boot Services ya no están disponibles. Sus funciones son: leer, escribir y eliminar variables persistentes del firmware que sobreviven entre reinicios, obtener y configurar la hora del hardware (RTC), solicitar al firmware un reinicio, apagado o cambio de modo y registrar fallos del sistema

Respecto UEFI y PI podemos diferenciar dos conceptos fundamentales: UEFI es puramente una especificación de interfaz. Define las APIs, estructuras de datos y el entorno pre-OS mediante el cual interactúan el firmware, los componentes de hardware y los cargadores del sistema operativo; UEFI define qué servicios están disponibles y cómo se accede a ellos. En cambio PI (Platform Initialization) es la arquitectura interna del firmware. Define cómo se construye la plataforma desde el momento del reset del hardware, estableciendo fases de control bien definidas hasta que se crea el entorno UEFI para el sistema operativo.

Etapas de PI:

- SEC (Security): Es la fase inicial pre-memoria. Establece un contexto mínimo de ejecución, configurando la memoria caché del procesador para usarla como RAM temporal (Cache-as-RAM) antes de que la memoria principal esté disponible. También establece la raíz de confianza inicial del sistema.
- PEI (Pre-EFI Initialization): Tiene como objetivo inicializar el hardware crítico mínimo, como el controlador de memoria principal y partes del chipset. También determina el modo de arranque y pasa la información descubierta a la siguiente fase mediante estructuras llamadas Hand-Off Blocks (HOBs).
- DXE (Driver Execution Environment): Es el núcleo de la inicialización. Un componente llamado DXE Dispatcher carga y ejecuta drivers en un orden determinado por sus dependencias lógicas. En esta fase se instalan la mayoría de las abstracciones de hardware, buses como PCI o USB, y los servicios centrales de UEFI.
- BDS (Boot Device Selection): Es donde el firmware decide la política de arranque basándose en variables almacenadas en NVRAM. Conecta los dispositivos de consola, expone dispositivos de almacenamiento o red y finalmente transfiere el control al cargador del sistema operativo.
- RT (Runtime): Comienza cuando el bootloader invoca ExitBootServices(). Esto finaliza el entorno de pre-arranque, libera la mayor parte de la memoria, pero conserva los Runtime Services que el sistema operativo puede seguir usando, como la manipulación de variables NVRAM o el control del reloj del sistema.

## Resultados

### Primera parte: Exploración del entorno UEFI y la Shell

En esta primera parte del trabajo práctico se explora cómo UEFI abstrae el hardware y gestiona la configuración antes de la carga del sistema operativo. Al ejecutar QEMU con el firmware OVMF, el sistema no inicia un sistema operativo, sino que ingresa directamente a la UEFI Shell, un entorno interactivo pre-OS.

En este estado inicial, al inspeccionar los dispositivos con el comando `map` se observa únicamente un dispositivo de tipo BLK0, lo que indica que el firmware detecta dispositivos a nivel de bloque pero no encuentra ningún sistema de archivos montado.

![Salida qemu sin imagen](https://github.com/user-attachments/assets/c4e8eef2-0b4b-474d-b7b8-6db16c34896e)

Dado que UEFI no trabaja directamente con dispositivos crudos, sino con abstracciones basadas en protocolos. Para que el firmware pueda exponer un sistema de archivos (FS0) y eventualmente cargar aplicaciones o bootloaders, se necesita proporcionar un dispositivo de almacenamiento que contenga un filesystem válido (FAT en nuestro caso). En QEMU, esto se logra mediante la creación y conexión explícita de una imagen de disco. Esto se hace ejecutando los siguientes comandos:

```bash
dd if=/dev/zero of=disk.img bs=1M count=64
mkfs.vfat -F 32 disk.img
```

Luego se ejecuta qemu especificando la imagen:

```bash
qemu-system-x86_64 -m 512 -bios /usr/share/ovmf/OVMF.fd -drive format=raw,file=disk.img -net none
```

Para entender esta primera parte debemos entender que es un handle y un protocolo:

Protocolo: Es básicamente una interfaz de software. A nivel técnico, es un bloque que contiene punteros a funciones y estructuras de datos. Cada protocolo está diseñado para realizar una tarea específica y se identifica invariablemente mediante un código único e irrepetible llamado GUID (Identificador Único Global).

Los protocolos definen qué es lo que se puede hacer. Por ejemplo, existe un protocolo llamado _SimpleFileSystem_. Cualquier cosa en UEFI que tenga este protocolo asociado, significa que tiene las funciones necesarias para que se pueda explorar carpetas y leer archivos dentro de él.

Handle: Es el identificador que representa a una entidad física o lógica concreta de la computadora, como puede ser un puerto USB, una partición de un disco duro, una tarjeta de red o driver (entidad lógica).

Los Handles actúan como "contenedores" donde se agrupan uno o más protocolos. Por ejemplo, el Handle que representa a un pendrive físico con formato FAT32, puede tener agrupados dentro de él, el protocolo de dispositivo de bloques (para leer sectores físicos) y el protocolo _SimpleFileSystem_ (por estar formateado en FAT32).

Cuando ejecutamos el comando ls, este opera sobre el handle FS0, el cual tiene asociado el protocolo _SimpleFileSystem_. El comando utiliza dicho protocolo para acceder al sistema de archivos y listar su contenido.

![Salida qemu con imagen cargada](https://github.com/user-attachments/assets/f1478e2f-9ff9-49e3-b740-d515fc89e21e)

Por otro lado, el comando dh (dump handle) permite visualizar la base de datos de handles del sistema, junto con los protocolos asociados a cada uno.

![Salida dh](https://github.com/user-attachments/assets/6d7c358b-969d-4586-b62b-b9392aceffcf)

Entre los protocolos podemos observar resaltado en verde _SimpleFileSystem_ que fue el que usa el comando `ls`

![Fin salida dh](https://github.com/user-attachments/assets/8887e2cd-a771-4fbc-a3d6-8173939388c9)

El comando set permite definir y gestionar variables de entorno dentro de la UEFI Shell. Estas variables son volátiles y existen únicamente durante la ejecución de la sesión, a diferencia de las variables UEFI almacenadas en NVRAM. Ale ejecutar `set TestSeguridad "Hola UEFI"` crea una variable de prueba, mientras que `set -v` permite visualizar las variables de entornos actualmente establecidas.

![Variables de entorno shell UEFI](https://github.com/user-attachments/assets/49752ea7-3332-461c-a510-7f3ccf50f08a)

`dmpstore` es una herramienta que permite ver variables UEFI almacenadas en NVRAM. A diferencia de set, acá ya se esta interactuando con el firmware real, no con la shell.

![Salida dmpstore](https://github.com/user-attachments/assets/6ae2477e-d41a-4f58-a162-1bfbb5646399)

De la salida podemos observar que la variable tiene los siguientes atributos:

- NV: Non Volatile (persiste entre reinicios)
- BS: accesible durante Boot Services
- RT: accesible en Runtime (post-boot)

Ademas la variable esta seteada como: `00 00 01 00 02 00`

Estos son enteros de 16 bits en little endian, por lo tanto se traduce como:

`BootOrder = [Boot0000, Boot0001, Boot0002]`

Esto es el orden en el que se va a intentar arrancar, primero Boot0000, si falla Boot0001, luego Boot0002

Ademas hay otra variable que indica que arranque se utilizo actualmente, indica `Boot0002` que corresponde justamente a la shell:

![Current Boot](https://github.com/user-attachments/assets/202b084e-f1a4-407d-9d83-673da9e40c02)

Al ejecutar el comando `memmap` podemos observar distintos rangos de memoria RAM. Cada rango tiene:

- Tipo: Indica el proposito de dicho rango
- Dirección de inicio-Dirección final
- Cantidad de paginas: cantidad de paginas que ocupa (cada pagina mide 4KB).
- Atributos

![memmap](https://github.com/user-attachments/assets/5f48a364-7798-4a2c-977f-581fdba509f8)

Los tipos pueden ser:

|  Tipo de Memoria  |                                                                                        Significado y Uso                                                                                         |
| :---------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|     Reserved      |                                              Memoria que el firmware o el hardware reserva para sí mismo. El sistema operativo no debería tocarla.                                               |
|  LoaderCode/Data  |                                                                            Memoria utilizada por el cargador del SO.                                                                             |
| BS_Code / BS_Data |                 Boot Services. Es memoria usada por drivers y aplicaciones durante el arranque. Se libera y queda disponible para el SO una vez que este toma el control total.                  |
| RT_Code / RT_Data | Runtime Services. Es memoria que persiste incluso después de que el sistema operativo ha cargado. Aquí residen funciones críticas como el acceso a variables de la NVRAM o el reloj del sistema. |
|  ACPI_Recl / NVS  |                                  Tablas ACPI que describen el hardware al SO. La parte Recl (Reclaimable) puede ser reutilizada por el SO tras leer las tablas.                                  |
|     Available     |                                         RAM pura y libre. Es el espacio donde el sistema operativo y tus programas pueden ejecutarse sin restricciones.                                          |
| MMIO / MMIO_Port  |                  Memoria mapeada para entrada/salida. No es RAM física real, sino "direcciones" que se comunican directamente con el hardware (como tu tarjeta de video o red).                  |

Las regiones RT_Code (Runtime Services Code) son extremadamente sensibles. Si un malware logra inyectarse ahí, puede sobrevivir incluso después de que se formatee el disco y se reinstale el SO, ya que reside en el mapa de memoria del firmware del disco duro, no en el almacenamiento del SO.

### Segunda parte: Desarrollo, compilación y análisis de seguridad

Para esta fase del proyecto, desarrollamos una aplicación nativa para el entorno UEFI (Unified Extensible Firmware Interface) escrita en lenguaje C. A diferencia de un programa convencional, este código se ejecuta en una etapa de _bare metal_, es decir, antes de que cualquier sistema operativo haya tomado el control del hardware.

```C
#include <efi.h>
#include <efilib.h>

EFI_STATUS efi_main(EFI_HANDLE ImageHandle, EFI_SYSTEM_TABLE *SystemTable) {
  InitializeLib(ImageHandle, SystemTable);
  SystemTable->ConOut->OutputString(SystemTable->ConOut,
                                    L"Iniciando analisis de seguridad...\r\n");
  // Inyección de un software breakpoint (INT3)
  unsigned char code[] = {0xCC};
  if (code[0] == 0xCC) {
    SystemTable->ConOut->OutputString(SystemTable->ConOut,
                                      L"Breakpoint estatico alcanzado.\r\n");
  }
  return EFI_SUCCESS;
}
```

Dado que el programa se ejecutará en un entorno previo al arranque de un sistema operativo, el programa debe ser autosuficiente, por lo tanto debe interactuar directamente con las tablas de servicios que el firmware mantiene en memoria estos son los protocolos estandarizado de UEFI.

La compilación se gestionó mediante objetivos configurados en un archivo Makefile que posteriormente son ejecutados por el programa make

Tras obtener el ejecutable en formato `.efi`, procedimos a su análisis mediante Ghidra, una suite de ingeniería inversa de código abierto desarrollada por la NSA. El foco del análisis se centró en la función `efi_main`, el punto de entrada estándar donde el firmware transfiere el control a nuestra aplicación.

Podemos observar el código ensamblador de nuestro programa:

![Ensamblador](https://github.com/user-attachments/assets/fc28fc2a-5ec8-4e4f-a500-ddfb73b454bb)

Ademas Ghidra proporciona decompilador que intenta reconstruir el codigo original a partir del ensamblador

![Decompiler](https://github.com/user-attachments/assets/5785872f-e6a5-4a04-9b22-50528a3201eb)

Si bien el descompilador de Ghidra facilita la comprensión de la lógica, al reconstruir una aproximación en lenguaje C. Las optimizaciones aplicadas durante la descompilación pueden omitir comprobaciones críticas o representar erróneamente tipos de datos, especialmente en entornos de bajo nivel como UEFI donde la gestión de punteros y estructuras de sistema es manual.

#### Técnicas de Anti-Debugging: Detección de Software Breakpoints (0xCC)

En el desarrollo de malware y software protegido, la inclusión de verificaciones basadas en el valor 0xCC tiene como objetivo detectar si un analista de seguridad está inspeccionando el código en tiempo de ejecución.

En la arquitectura x86-64, el byte 0xCC corresponde a la instrucción INT 3. Esta es la herramienta fundamental que utilizan los depuradores (como GDB) para pausar la ejecución de un programa. Cuando un analista coloca un "punto de interrupción" o breakpoint, el depurador reemplaza temporalmente el byte original de una instrucción por un 0xCC

Los autores de malware implementan comprobaciones similares a la realizada en nuestro programa en C para verificar su propia integridad, por ejemplo hacer que el programa recorra sus propias secciones de código (.text) buscando el byte 0xCC, y si lo encuentra, asume que ha sido manipulado por un depurador. Luego al detectar la presencia de un breakpoint, el malware puede ejecutar rutinas de evasión, como finalizar su proceso, corromper su propio código o mostrar mensajes falsos para engañar al investigador.

En nuestro experimento, el uso de `unsigned char code[] = {0xCC}` funciona como un testigo de memoria. Si bien no detiene el programa porque se trata como un dato y no como una instrucción ejecutable, sirve para demostrar cómo estas firmas pueden ser detectadas tanto por el software mismo como por herramientas de análisis estático como Ghidra

Desde la perspectiva del análisis, estas comprobaciones presentan dos desafíos:

1. Ofuscación: En el descompilador de Ghidra, este valor puede aparecer erróneamente como -52 debido a la interpretación de tipos con signo, lo que podría ocultar la verdadera intención del código ante un analista inexperto.

2. Optimización: Como se observó en nuestro análisis, los compiladores modernos pueden optimizar o eliminar estas condiciones si detectan que son constantes, lo que obliga al analista a recurrir siempre al código ensamblador (Listing) para confirmar la existencia de la protección.

### Tercera parte: Ejecución en Hardware Físico (Bare Metal)

Para esta ultima parte vamos a instalar UEFI Shell de TianoCore y ejecutaremos el programa en la computadora usando un pendrive

Usando lsblk identificamos nuestro pendrive y sus particiones (En mi caso es /dev/sda1.)

```bash
lsblk
```

Lo montamos en una carpeta, en nuestro caso en /mnt:

```bash
sudo mount /dev/sda1 /mnt
```

Creamos la estructura estandarizada de directorios

```bash
sudo mkdir -p /mnt/EFI/BOOT
```

Descargamos dentro la UEFI Shell de TianoCore

```bash
sudo wget
https://github.com/tianocore/edk2/raw/UDK2018/ShellBinPkg/UefiShell/X64/Shell.efi -O
/mnt/EFI/BOOT/BOOTX64.EFI
```

y finalmente guardamos el programa dentro del pendrive y lo desmontamos

```bash
cp aplicacion.efi /mnt
sudo sync
sudo umount /mnt
```

Booteamos el pendrive y dentro de la UEFI Shell ejecutamos el programa:

![Ejecución del programa](https://github.com/user-attachments/assets/882bb7e1-e703-47a6-bf50-be508f996755)
