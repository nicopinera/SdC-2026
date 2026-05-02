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

<!-- Aca poner una introduccion sobre UEFI, cuando se desarrolla, porque y que remplaza (BIOS) -->

<!-- Diferencia entre UEFI y PI, etapas de PI, copiaria literal como esta en la presentación de TP -->

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

Los protocolos definen qué es lo que se puede hacer. Por ejemplo, existe un protocolo llamado *SimpleFileSystem*. Cualquier cosa en UEFI que tenga este protocolo asociado, significa que tiene las funciones necesarias para que se pueda explorar carpetas y leer archivos dentro de él.

Handle: Es el identificador que representa a una entidad física o lógica concreta de la computadora, como puede ser un puerto USB, una partición de un disco duro, una tarjeta de red o driver (entidad lógica).

Los Handles actúan como "contenedores" donde se agrupan uno o más protocolos. Por ejemplo, el Handle que representa a un pendrive físico con formato FAT32, puede tener agrupados dentro de él, el protocolo de dispositivo de bloques (para leer sectores físicos) y el protocolo *SimpleFileSystem* (por estar formateado en FAT32).

Cuando ejecutamos el comando ls, este opera sobre el handle FS0, el cual tiene asociado el protocolo *SimpleFileSystem*. El comando utiliza dicho protocolo para acceder al sistema de archivos y listar su contenido.

![Salida qemu con imagen cargada](https://github.com/user-attachments/assets/f1478e2f-9ff9-49e3-b740-d515fc89e21e)

Por otro lado, el comando dh (dump handle) permite visualizar la base de datos de handles del sistema, junto con los protocolos asociados a cada uno.

![Salida dh](https://github.com/user-attachments/assets/6d7c358b-969d-4586-b62b-b9392aceffcf)

Entre los protocolos podemos observar resaltado en verde *SimpleFileSystem* que fue el que usa el comando `ls`

![Fin salida dh](https://github.com/user-attachments/assets/8887e2cd-a771-4fbc-a3d6-8173939388c9)

El comando set permite definir y gestionar variables de entorno dentro de la UEFI Shell. Estas variables son volátiles y existen únicamente durante la ejecución de la sesión, a diferencia de las variables UEFI almacenadas en NVRAM. Ale ejecutar `set TestSeguridad "Hola UEFI"` crea una variable de prueba, mientras que `set -v` permite visualizar las variables de entornos actualmente establecidas.

![Variables de entorno shell UEFI](https://github.com/user-attachments/assets/49752ea7-3332-461c-a510-7f3ccf50f08a)

`dmpstore` es una herramienta que permite ver variables UEFI almacenadas en NVRAM. A diferencia de set, acá ya se esta interactuando con el firmware real, no con la shell.

![Salida dmpstore](https://github.com/user-attachments/assets/6ae2477e-d41a-4f58-a162-1bfbb5646399)

De la salida podemos observar que la variable tiene los siguientes atributos:

NV: Non Volatile (persiste entre reinicios)
BS: accesible durante Boot Services
RT: accesible en Runtime (post-boot)

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

|Tipo de Memoria |Significado y Uso|
|:--------------:|:---------------:|
|Reserved        |Memoria que el firmware o el hardware reserva para sí mismo. El sistema operativo no debería tocarla.|
|LoaderCode/Data | Memoria utilizada por el cargador del SO.|
|BS_Code / BS_Data | Boot Services. Es memoria usada por drivers y aplicaciones durante el arranque. Se libera y queda disponible para el SO una vez que este toma el control total.|
|RT_Code / RT_Data | Runtime Services. Es memoria que persiste incluso después de que el sistema operativo ha cargado. Aquí residen funciones críticas como el acceso a variables de la NVRAM o el reloj del sistema.|
|ACPI_Recl / NVS | Tablas ACPI que describen el hardware al SO. La parte Recl (Reclaimable) puede ser reutilizada por el SO tras leer las tablas.|
|Available       | RAM pura y libre. Es el espacio donde el sistema operativo y tus programas pueden ejecutarse sin restricciones.|
|MMIO / MMIO_Port | Memoria mapeada para entrada/salida. No es RAM física real, sino "direcciones" que se comunican directamente con el hardware (como tu tarjeta de video o red).|

Las regiones RT_Code (Runtime Services Code) son extremadamente sensibles. Si un malware logra inyectarse ahí, puede sobrevivir incluso después de que se formatee el disco y se reinstale el SO, ya que reside en el mapa de memoria del firmware del disco duro, no en el almacenamiento del SO.