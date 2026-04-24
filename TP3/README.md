# Trabajo práctico 3 - Modo protegido

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

¿Qué es UEFI? ¿Cómo puedo usarlo? Mencionar además una función a la que podría llamar usando esa dinámica.

UEFI (Unified Extensible Firmware Interface), es la interfaz entre el firmware de la placa madre y el sistema operativo; se encarga de inicializar el hardware, gestionar el arranque y ofrecer servicios al SO.

En el contexto de arranque de modo protegido del CPU que luego "evoluciona", UEFI es quien orquesta esa transición. Lleva el procesador del modo real al modo protegido y luego al long mode 64 bits.

UEFI se puede usar desde el código; cuenta con una tabla llamada EFI_SYSTEM_TABLE, que contiene punteros a funciones que podés llamar desde una aplicación UEFI. Estas funciones permiten acceder a la pantalla, teclado, sistema de archivos, etc., antes de que el sistema operativo esté cargado.

Se podría llamar por ejemplo a la función OuputString. Esta función es uno de los Boot Services de UEFI: disponible sólo durante el arranque.

---

Menciona casos de bugs de UEFI que puedan ser explotados.

LogoFAIL (2023): Familia de vulnerabilidades en los parsers de imágenes del firmware UEFI (BMP, PNG, GIF). Durante el arranque UEFI muestra el logo del fabricante, si ese archivo de imagen es reemplazado por uno malicioso, el parser buggeado ejecuta código arbitrario por debajo del sistema operativo, invisible para antivirus.

ThinkPwn / SMM vulnerabilities: Aplicado a Drivers de dispositivos. Bugs en el System Management Mode (SMM), un modo de CPU aún más privilegiado que el kernel. Explotar SMM permite escribir en la flash del firmware para lograr persistencia total. Sobrevive a reinstalaciones del OS y al reemplazo del disco.

---

¿Qué es Converged Security and Management Engine (CSME), the Intel Management Engine BIOS Extension (Intel MEBx)?

CSME es un subsistema autónomo integrado en los chipsets Intel que funciona de manera completamente independiente al CPU principal. Cuenta con su propio procesador (ARC/x86 de 32 bits), su propia RAM, su propio sistema operativo; y acceso directo a la red, memoria y almacenamiento incluso con el equipo apagado,o mientras haya energía en standby. Lo clave del CSME es su posición en la jerarquía de privilegios: corre por debajo del sistema operativo, debajo del hypervisor y por debajo del SMM. Es el componente con mayor acceso al hardware.

Por otro lado, Intel MEBx (Management Engine BIOS Extension) es la interfaz de configuración del CSME. Es una interfaz de texto que aparece durante el POST y permite configurar qué capacidades de AMT están habilitadas, con qué credenciales, y en qué red opera. Es accesible previo a la carga del SO.

---

¿Qué es coreboot? ¿Qué productos lo incorporan? ¿Cuáles son las ventajas de su utilización?

Coreboot es un firmware de código abierto que reemplaza al BIOS/UEFI propietario. Intenta hacer lo mínimo en firmware y delegar el resto a un payload. Es, escencialmente, un núcleo de arranque.

Productos que lo incorporan: Google Chromebooks y ChromeOS Flex, System76, Framework Laptop y también servidores de Google.

Algunas ventajas que presenta su utilización:

1. Al ser código abierto cualquiera puede revisar qué hace exactamente el firmware, con UEFI propietario eso es imposible.

2. Coreboot hace sustancialmente menos cosas que un UEFI completo.

3. Sin el overhead de las fases SEC/PEI/DXE/BDS, coreboot puede entregar el control al SO en 1–3 segundos en lugar de los 20–60 habituales de un UEFI propietario.

---

#### ¿Que es un linker? ¿que función cumple?

El linker (ld) es la etapa posterior al ensamblado/compilación. Toma uno o más archivos objeto (.o) y construye un binario final tiene diversas funciones:

- Resolución de símbolos: Proceso mediante el cual el linker asocia identificadores simbólicos (nombres de funciones, variables, etiquetas) con sus definiciones reales. Si un símbolo es declarado en un módulo y definido en otro, el linker conecta ambas referencias y sustituye el nombre por su dirección o ubicación final.

- Asignación de direcciones: El linker determina en qué direcciones de memoria se ubicará cada parte del programa. Esto implica asignar rangos de direcciones a secciones como código, datos y pila, respetando restricciones de alineación y convenciones del formato ejecutable o del entorno de ejecución.

- Layout del binario: Se refiere a la organización interna del archivo generado: el orden y disposición de secciones, su tamaño, alineación y offsets dentro del binario. Define cómo se representa el programa como una secuencia de bytes, independientemente de cómo se cargará en memoria.

- Relocalización: Mecanismo mediante el cual el linker (en algunos casos el loader) ajusta las referencias a direcciones dentro del código y los datos para que sean correctas según la ubicación final en memoria. Esto permite que el código funcione correctamente incluso si no se conoce su dirección exacta en etapas tempranas de compilación.

La etapa de enlazamiento o linkeo es la ultima del proceso de compilación, produce es un archivo ELF o un binario plano como en nuestro caso

---

#### ¿Que es la dirección que aparece en el script del linker? ¿Por qué es necesario?

La dirección `0x7C00` corresponde a la dirección física en memoria donde la BIOS carga el primer sector de arranque del dispositivo seleccionado. Cuando se arranca desde un disco, la BIOS copia los primeros 512 bytes del disco a esa dirección. Es por esto que el linker script usa esa dirección, el código debe estar ensamblado como si fuera a ejecutarse allí, ya que efectivamente la CPU comenzará a ejecutarlo desde esa ubicación tras el arranque.

---

#### Compare la salida de objdump con hexdump, verifique donde fue colocado el programa dentro de la imagen.

Salida de objdump:

Como podemos observar en la primera línea, el operando inmediato de `mov` (`be`) aparece como `00 00` porque en el archivo objeto (`.o`) la dirección del símbolo `msg` todavía no fue resuelta. Esto sucede porque el `.o` es un archivo relocatable, es decir, aún no tiene direcciones finales asignadas. La instrucción `mov $msg, %si` depende de conocer la dirección exacta de `msg`, pero en esta etapa el ensamblador no sabe dónde quedará ubicado en memoria. Por ese motivo, deja un valor placeholder (`0x0000`) y registra información de relocalización para que el linker pueda corregirlo más adelante. Luego durante el proceso de linking, el linker asigna direcciones reales, calcula la dirección final de msg y reemplaza ese valor incompleto por el correcto.

![object dump del programa ensamblado](https://github.com/user-attachments/assets/1cba194b-fbc0-444f-9561-48e978e8bedf)

Salida de hexdump:

En los primeros bytes (arriba a la izquierda) se observa que la instrucción `mov` ya tiene el operando inmediato correctamente resuelto, en este caso `0x7C0F`, que corresponde a la dirección donde se encuentra `msg`. Esto tiene sentido porque en el linker script se definió que el programa debía ubicarse a partir de la dirección `0x7C00`. Como msg está a un offset de aproximadamente `0x0F` dentro del programa, el linker calcula su dirección final como `0x7C00 + 0x0F = 0x7C0F` y reemplaza el valor inmediato en la instrucción.

![hexdump del binario generado](https://github.com/user-attachments/assets/b4f80063-5d56-43d5-b1c1-6f68b1a37a69)

---

#### Grabar la imagen en un pendrive y probarla en una pc y subir una foto

<!-- Por ahora no se pudo hacer andar en pc :( -->

---

#### ¿Para que se utiliza la opción `--oformat binary` en el linker?

La opción `--oformat binary` en el linker indica que la salida debe ser un binario plano (flat binary), es decir, una secuencia de bytes sin ningún tipo de estructura adicional. Por defecto, el linker genera archivos en formato ELF, que incluyen metadata como encabezados (ELF header), tablas de segmentos (program headers), tablas de secciones, símbolos, etc. En este caso no se utiliza ELF porque el programa no será cargado por un sistema operativo, sino directamente por la BIOS, que espera encontrar código ejecutable en formato crudo dentro del sector de arranque. Por lo tanto, es necesario eliminar toda esa metadata y dejar únicamente los bytes que la CPU va a ejecutar.

---

## Referencias
