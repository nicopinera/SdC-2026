# Trabajo práctico 3-A - Modo protegido

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

**Fecha:** 27/4/2026

---

## Información de los autores

- **Información de contacto**:
  - [nicolas.pinera@mi.unc.edu.ar](mailto:nicolas.pinera@mi.unc.edu.ar)
  - [julian.krede@mi.unc.edu.ar](mailto:julian.krede@mi.unc.edu.ar)
  - [juana.pucheta.noguera@mi.unc.edu.ar](mailto:juana.pucheta.noguera@mi.unc.edu.ar)

---

## Introducción

## Resultados

### Qué es UEFI y Cómo puedo usarlo

**UEFI** (Unified Extensible Firmware Interface), es una capa de software de bajo nivel que reside en un chip dentro de la placa base. Se encarga de inicializar los componentes de hardware (procesador, memoria, almacenamiento), gestionar el arranque y verificar que todo esté en orden antes de entregarle el control al sistema operativo. Es el sucesor directo del antiguo **BIOS**, diseñado para superar las limitaciones de este último y ofrecer un arranque más rápido y seguro.

La interacción con la UEFI se da principalmente de **dos** maneras:

1. **Acceso al Menú de Configuración**: Para realizar ajustes manuales (como cambiar el orden de arranque o activar la virtualización), se debe acceder a su interfaz antes de que cargue el sistema operativo. Reiniciando la computadora y apretando una tecla especifica que indica la PC en pantalla cuando esta iniciando.
2. **Servicios de Tiempo de Ejecución (Runtime Services)**: Estos servicios permanecen activos y disponibles en la RAM incluso cuando ya estás usando el Sistema Operativo. Permiten que el sistema operativo y el firmware sigan comunicándose sin reiniciar. Mediante los Runtime Services, el sistema operativo puede leer o escribir en esa libreta en cualquier momento.

Cuando una CPU se enciende, comienza en un estado muy básico. La UEFI se encarga de cambiar el procesador de **Modo Real** (un modo limitado de 16 bits) a **Modo Protegido** (32 bits) o **Modo Largo** (64 bits).

UEFI se puede usar desde el código; cuenta con una tabla llamada **EFI_SYSTEM_TABLE**, que contiene punteros a funciones que podés llamar desde una aplicación UEFI. Estas funciones permiten acceder a la pantalla, teclado, sistema de archivos, etc., antes de que el sistema operativo esté cargado.Una dinámica común al trabajar con UEFI es la consulta de Variables de Entorno. Una función fundamental a la que un programador o el sistema operativo puede llamar es: **GetVariable**. Esta función permite leer datos almacenados en la memoria no volátil (NVRAM) de la placa base.

### Casos de bugs de UEFI que puedan ser explotados

Debido a que la UEFI reside en una capa inferior al sistema operativo y tiene privilegios totales sobre el hardware, un bug en este nivel es extremadamente peligroso: permite la persistencia de malware incluso si se formatea el disco duro o se reinstala el sistema operativo.

**LogoFAIL (2023):** Familia de vulnerabilidades en los parsers de imágenes del firmware UEFI (BMP, PNG, GIF). Durante el arranque UEFI muestra el logo del fabricante, si ese archivo de imagen es reemplazado por uno malicioso, el parser buggeado ejecuta código arbitrario por debajo del sistema operativo, invisible para antivirus.

**ThinkPwn / SMM vulnerabilities**: Aplicado a Drivers de dispositivos. Bugs en el System Management Mode (SMM), un modo de CPU aún más privilegiado que el kernel. Explotar SMM permite escribir en la flash del firmware para lograr persistencia total. Sobrevive a reinstalaciones del OS y al reemplazo del disco.

### Converged Security and Management Engine (CSME), the Intel Management Engine BIOS Extension (Intel MEBx)

**CSME** es un subsistema autónomo integrado en los chipsets Intel que funciona de manera completamente independiente al CPU principal. Cuenta con su propio procesador (ARC/x86 de 32 bits), su propia RAM, su propio sistema operativo (basado en MINIX); y acceso directo a la red, memoria y almacenamiento incluso con el equipo apagado, o mientras haya energía en standby. Lo clave del CSME es su posición en la jerarquía de privilegios: corre por debajo del sistema operativo, debajo del hypervisor y por debajo del SMM. Es el componente con mayor acceso al hardware. Se encarga de la autenticación del firmware, la gestión de claves criptográficas y la ejecución de funciones de seguridad que la CPU principal no debe tocar.

Por otro lado, **Intel MEBx (Management Engine BIOS Extension)** es la interfaz de configuración del CSME. Es una interfaz de texto que aparece durante el POST y permite configurar qué capacidades de AMT están habilitadas, con qué credenciales, y en qué red opera. Es accesible previo a la carga del SO.

### Coreboot, productos que lo incorporan y sus ventajas

**Coreboot** (anteriormente conocido como LinuxBIOS) es un proyecto de software de código abierto diseñado para realizar la mínima inicialización de hardware necesaria antes de ceder el control a un software secundario llamado Payload. Intenta hacer lo mínimo en firmware y delegar el resto a un payload. Es, escencialmente, un núcleo de arranque.

- Productos que lo incorporan: Google Chromebooks y ChromeOS Flex, System76, Framework Laptop y también servidores de Google.

Algunas ventajas que presenta su utilización:

1. Al ser código abierto cualquiera puede revisar qué hace exactamente el firmware, con UEFI propietario eso es imposible.
2. Coreboot hace sustancialmente menos cosas que un UEFI completo.
3. Sin el overhead de las fases SEC/PEI/DXE/BDS, coreboot puede entregar el control al SO en 1–3 segundos en lugar de los 20–60 habituales de un UEFI propietario.

### El Linker

El linker (ld) es la etapa posterior al ensamblado/compilación. Toma uno o más archivos objeto (.o) generados por el compilador y construye un binario final tiene diversas funciones:

- **Resolución de símbolos**: Los programas suelen estar divididos en múltiples archivos y dependen de bibliotecas externas. Este proceso es mediante el cual el linker asocia identificadores simbólicos (nombres de funciones, variables, etiquetas) con sus definiciones reales. Si un símbolo es declarado en un módulo y definido en otro, el linker conecta ambas referencias y sustituye el nombre por su dirección o ubicación final.

- **Asignación de direcciones**: El linker determina en qué direcciones de memoria se ubicará cada parte del programa. Esto implica asignar rangos de direcciones a secciones como código, datos y pila, respetando restricciones de alineación y convenciones del formato ejecutable o del entorno de ejecución.

- **Layout del binario**: Se refiere a la organización interna del archivo generado, el orden y disposición de secciones, su tamaño, alineación y offsets dentro del binario. Define cómo se representa el programa como una secuencia de bytes, independientemente de cómo se cargará en memoria.

- **Relocalización**: Mecanismo mediante el cual el linker (en algunos casos el loader) ajusta las referencias a direcciones dentro del código y los datos para que sean correctas según la ubicación final en memoria. Esto permite que el código funcione correctamente incluso si no se conoce su dirección exacta en etapas tempranas de compilación.

La etapa de enlazamiento o linkeo es la ultima del proceso de compilación, produce es un archivo ELF o un binario plano como en nuestro caso.

### La dirección `0x7C00` en el script del linker

La dirección `0x7C00` corresponde a la dirección física en memoria donde la BIOS carga el primer sector de arranque del dispositivo seleccionado. Cuando se arranca desde un disco, la BIOS copia los primeros 512 bytes del disco a esa dirección. Es por esto que el [linker script](/TP3/link.ld) usa esa dirección, el código debe estar ensamblado como si fuera a ejecutarse allí, ya que efectivamente la CPU comenzará a ejecutarlo desde esa ubicación tras el arranque.

### Comparación entre salida de objdump con hexdump

#### Salida de objdump

Como podemos observar en la primera línea, el operando inmediato de `mov` (`be`) aparece como `00 00` porque en el archivo objeto (`.o`) la dirección del símbolo `msg` todavía no fue resuelta. Esto sucede porque el `.o` es un archivo relocatable, es decir, aún no tiene direcciones finales asignadas. La instrucción `mov $msg, %si` depende de conocer la dirección exacta de `msg`, pero en esta etapa el ensamblador no sabe dónde quedará ubicado en memoria. Por ese motivo, deja un valor placeholder (`0x0000`) y registra información de relocalización para que el linker pueda corregirlo más adelante. Luego durante el proceso de linking, el linker asigna direcciones reales, calcula la dirección final de msg y reemplaza ese valor incompleto por el correcto.

![object dump del programa ensamblado](https://github.com/user-attachments/assets/1cba194b-fbc0-444f-9561-48e978e8bedf)

#### Salida de hexdump

En los primeros bytes (arriba a la izquierda) se observa que la instrucción `mov` ya tiene el operando inmediato correctamente resuelto, en este caso `0x7C0F`, que corresponde a la dirección donde se encuentra `msg`. Esto tiene sentido porque en el linker script se definió que el programa debía ubicarse a partir de la dirección `0x7C00`. Como msg está a un offset de aproximadamente `0x0F` dentro del programa, el linker calcula su dirección final como `0x7C00 + 0x0F = 0x7C0F` y reemplaza el valor inmediato en la instrucción.

![hexdump del binario generado](https://github.com/user-attachments/assets/b4f80063-5d56-43d5-b1c1-6f68b1a37a69)

### Grabar la imagen en un pendrive y probarla en una pc y subir una foto
Para realizar esta parte tuvimos que modificar un poco el programa que se nos provee para que funcione correctamente, las cosas que se le agrego al programa son:
1. Inicializacion de registros de datos y stack
2. Limpieza de la pantalla y establecimiento en modo texto
3. Configuracion de registros para imprimir: Normalización de video para limpiar el estado previo del hardware, y definición estricta de parámetros de registros para garantizar que la BIOS ejecute la impresión de forma visible y predecible.

Primero compilamos el programa:

```bash
as -g -o main.o main.S
ld --oformat binary -o main.img -T link.ld main.o
```
Verificamos como aparece nuestro pendrive en el sistema con lsblk:

```bash
lsblk
```

Luego lo grabamos en el pendrive con dd:

```bash
sudo dd if=main.img of=/dev/sda bs=446 count=1 conv=notrunc
```
Finalmente asegurandonos que nuestro sistema de arranque permita legacy boot, para poder ejecutar el pendrive, y ejecutamos el pendrive:

![foto monitor](https://github.com/user-attachments/assets/b0e6d59a-857f-4982-85e7-32f1844e15d5)

### ¿Para que se utiliza la opción `--oformat binary` en el linker?

La opción `--oformat binary` en el linker indica que la salida debe ser un binario plano (flat binary), es decir, una secuencia de bytes sin ningún tipo de estructura adicional. Por defecto, el linker genera archivos en formato ELF, que incluyen metadata como encabezados (ELF header), tablas de segmentos (program headers), tablas de secciones, símbolos, etc. En este caso no se utiliza ELF porque el programa no será cargado por un sistema operativo, sino directamente por la BIOS, que espera encontrar código ejecutable en formato crudo dentro del sector de arranque. Por lo tanto, es necesario eliminar toda esa metadata y dejar únicamente los bytes que la CPU va a ejecutar.

---

### Modo protegido y registro de segmentos

En el **Modo Protegido**, los registros de segmento _(CS, DS, SS, ES, FS, GS)_ ya no contienen una dirección base de memoria física (como ocurría en el Modo Real). En su lugar, se cargan con un valor denominado **Selector de Segmento**. Un **Selector de Segmento** es un valor de 16 bits con la siguiente estructura interna:

- **Índice**: Selecciona una entrada específica dentro de una tabla de descriptores.
- **TI**: Indica si se debe buscar en la Tabla Global de Descriptores (GDT) o en la Local (LDT).
- **RPL**: Define el nivel de privilegio (Ring 0 a Ring 3) con el que se intenta acceder.

El cambio de "dirección" a "selector" responde a la necesidad de implementar seguridad y virtualización de la memoria. Las razones técnicas principales son:

1. **Indirección y Control de Acceso**: En **Modo Real**, cualquier programa podía escribir en cualquier dirección de memoria simplemente cambiando el registro de segmento. En **Modo Protegido**, el registro de segmento apunta a una entrada en la GDT (Global Descriptor Table). Esta entrada (el Descriptor de Segmento) contiene: La **Dirección Base real**, El **Límite** (tamaño máximo del segmento) y Los **Derechos de Acceso** (si es de solo lectura, ejecutable, etc.). La CPU verifica estos permisos antes de permitir el acceso a la RAM. Si el programa intenta escribir en un segmento marcado como "solo lectura", la CPU genera una **excepción** de protección general.

2. **Separación de Memoria Lógica y Física**: El uso de selectores permite que el Sistema Operativo mueva datos en la RAM física sin que el programa se de cuenta. El programa sigue usando el mismo "Selector", pero el Sistema Operativo actualiza la dirección base en la tabla GDT. Esto es la base de la relocalización dinámica.

3. **Implementación de los Anillos de Privilegio (Protection Rings)**: El valor cargado en el registro de segmento incluye el RPL. Esto permite a la CPU comparar el privilegio del código que se intenta ejecutar con el privilegio del segmento al que intenta acceder, impidiendo que una aplicación de usuario (Ring 3) acceda directamente a la memoria del núcleo o del firmware UEFI (Ring 0).

---

### Pasaje de modo real a modo protegido sin usar macros:

Para pasar de modo real a modo protegido a mano requiere configurar correctamente estructuras del procesador que normalmente abstraen los compiladores/bootloaders:

1. Deshabilitar interrupciones: ejecutar la instruccion cli, esto evita que una IRQ use estructuras aún no válidas.

```NASM
cli
```

2. Habilitar línea A20: Necesaria para direccionar más de 1 MB. Esto se puede hacer mediante el puerto 0x92:

```NASM
in al, 0x92
or al, 00000010b
out 0x92, al
```
3. Definir la tabla global de descriptores de segmento (GDT). Se requiere al menos:
- El Descriptor nulo
- El Segmento código (base 0, límite 4GB, ejecutable)
- El Segmento datos (base 0, límite 4GB, writable)

```NASM
gdt_start:

gdt_null:
    dq 0x0000000000000000
; En este caso tanto el segmento de codigo como datos
; acceden al mismo espacio lineal
gdt_code:
    dq 0x00CF9A000000FFFF

gdt_data:
    dq 0x00CF92000000FFFF

gdt_end:
```

```NASM
gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start
```
4. Cargar la dirección en el registro GDTR:

```NASM
lgdt [gdt_descriptor]
```
5. Activar bit PE (Protection Enable) en CR0

```NASM
mov eax, cr0
or eax, 1
mov cr0, eax
```
6. Hacer un Far jump: Esto limpia el pipeline y carga CS con selector válido de la GDT.

```NASM
jmp 0x08:protected_mode_entry
```
7. Cambiar a código de 32 bits y reconfigurar segmentos DS, ES, SS, etc.

```NASM
[bits 32]

protected_mode_entry:

mov ax, 0x10
mov ds, ax
mov es, ax
mov ss, ax
mov fs, ax
mov gs, ax
```
9. Inicializar el stack

```NASM
mov esp, 0x90000
```
---

### Separación de descriptores
Para romper el esquema de "modelo plano" (donde todos los segmentos comparten la base 0), se asignan regiones de memoria diferenciadas a los descriptores de código y datos. Esto permite que el hardware aísle los datos de las instrucciones, incrementando la seguridad y el orden del sistema.

En el archivo `segmentos_separados.asm`, definimos la tabla de la siguiente manera:
```NASM
gdt_start:
    dq 0x0000000000000000   ; Descriptor nulo obligatorio

; Segmento de código (Base = 0x00000000)
gdt_code:
    dw 0xFFFF              ; Límite [15:0]
    dw 0x0000              ; Base [15:0]
    db 0x00                ; Base [23:16]
    db 10011010b           ; Atributos de código
    db 11001111b           ; Granularidad y Límite [19:16]
    db 0x00                ; Base [31:24]


gdt_data:
    dw 0xFFFF
    dw 0x0000
    db 0x02                ; Base [23:16] (0x02 << 16 = 0x00020000)
    db 10010010b           ; Atributos de datos
    db 11001111b
    db 0x00
gdt_end:
```

#### Atributos de los Segmentos

1. Segmento de código (10011010b):

P (Present) = 1: El segmento está cargado en la memoria física.
DPL (Privilege) = 00: Nivel de privilegio máximo (Ring 0 / Kernel).
S (System) = 1: Indica que es un descriptor de código o datos (no de sistema como una TSS).

Tipo (1010b):
1: Segmento de codigo.
0: No conforme (No permite ejecución desde privilegios menores).
1: Lectura permitida (Permite leer constantes del segmento de código).
0: Accessed (Bit que el CPU pone en 1 tras el primer acceso).

1. Segmento de datos (10010010b):

P, DPL, S: Son Idénticos al de código para operar en el mismo nivel de privilegio.

Tipo (0010b):
0: Segmento de datos.
0: Expand-up (Direccionamiento normal hacia arriba).
1: Escribible (Permite operaciones mov [mem], reg).
0: Accessed.

A partir de la activación del modo protegido, la MMU (Memory Management Unit) calcula la ubicación física de cada dato mediante la fórmula:

$$\large \text{Dirección Lineal} = \text{Base del Segmento} + \text{Offset}$$

Para que este esquema sea funcional, debemos considerar dos escenarios:

1. Alineación del Código: Si decidimos cambiar la base del segmento de código en la GDT (por ejemplo, a 0x100000), el código físicamente debe residir en esa dirección antes de realizar el salto largo (`jmp selector:offset`). En un bootloader, esto requeriría copiar el sector cargado por el BIOS desde `0x7C00` a la nueva base usando instrucciones como `rep movsb` en modo real.

2. Ubicación de los Datos: Dado que el segmento de datos tiene base 0x00020000, cualquier acceso a una variable o dirección absoluta se verá desplazado. Por ejemplo:

```NASM
mov ax, 0x10    ; Selector de datos (Base 0x20000)
mov ds, ax
mov dword [0], 0xCAFEBABE
```

La instrucción anterior no escribe en la dirección física 0x0, sino en la dirección física 0x00020000. Esto demuestra que la segmentación permite abstraer las direcciones lógicas que usa el programador de las direcciones físicas reales del hardware.

---

### Experimento: Cambio del bit de acceso al segmento de datos
En esta etapa, modificamos el descriptor del segmento de datos en la GDT para restringir los permisos de escritura. El objetivo es observar cómo reacciona la arquitectura x86 cuando el software intenta violar las reglas de protección de memoria definidas en la tabla de descriptores.Para ello, cambiamos el byte de acceso de `10010010b` (Lectura/Escritura) a `10010000b` (Solo Lectura)
```NASM
gdt_data_ro:
    dw 0xFFFF                   ; Límite [15:0]
    dw 0x0000                   ; Base [15:0]
    db 0x00                     ; Base [23:16]
    db 10010000b                ; Atributos: El bit 1 (W) se establece en 0
    db 11001111b                ; Flags (Granularidad y Límite)
    db 0x00                     ; Base [31:24]
```

Utilizando GDB y los logs de QEMU, podemos analizar el colapso del sistema paso a paso:

Al iniciar, el procesador se encuentra en Modo Real. Ponemos un breakpoint en 0x7c00, que es la dirección física donde el BIOS carga nuestro sector de arranque.

![gdb inicio](https://github.com/user-attachments/assets/2acc3e48-f0c4-4110-9fd4-03e6c330ac56)

Avanzamos por las instrucciones que habilitan la línea A20 y preparan la carga de la GDT mediante la instrucción lgdt. En este punto, el registro interno GDTR ya conoce la ubicación y el tamaño de nuestra tabla.

![carga del gdt](https://github.com/user-attachments/assets/9a7f8d4b-66e5-4b19-9afb-0fbb470f6a7b)

Procedemos a activar el bit PE (Protection Enable) del registro CR0.

![Habilitacion de PE](https://github.com/user-attachments/assets/8e45f6c8-9bd7-4dba-acf9-a99c524406a6)

Al intentar ejecutar la instrucción `mov dword [0x500], 0xDEADBEEF`, el procesador consulta los derechos de acceso del segmento en el shadow register y detecta que la escritura está prohibida.

![Intento de carga de dato](https://github.com/user-attachments/assets/649c810b-383e-48cf-972d-0db648ad1ccd)

En la terminal de QEMU, observamos el registro de interrupciones que confirma el error:

`check_exception old: 0xffffffff new 0xd`
`check_exception old: 0xd new 0xd`
`check_exception old: 0x8 new 0xd`


![Salida qemu](https://github.com/user-attachments/assets/d1c7ac90-0666-4ba6-89c0-27bad5c707b6)

0xd (13) *#GP (General Protection Fault)*: Es la excepción principal, se dispara porque intentamos escribir en un segmento de datos que no tiene el bit W (Writable) activo.

0x8	*#DF (Double Fault)*: Al no tener una IDT (Interrupt Descriptor Table) configurada, el CPU no puede encontrar el manejador para el #GP. Esto genera una segunda falla al intentar procesar la primera.

Finalmente, al no poder manejar el Double Fault, se produce el Triple Fault y la CPU se reinicia (Reset).