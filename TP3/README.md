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

---------------------------------------------------------------------------------
Menciona casos de bugs de UEFI que puedan ser explotados.

LogoFAIL (2023): Familia de vulnerabilidades en los parsers de imágenes del firmware UEFI (BMP, PNG, GIF). Durante el arranque UEFI muestra el logo del fabricante, si ese archivo de imagen es reemplazado por uno malicioso, el parser buggeado ejecuta código arbitrario por debajo del sistema operativo, invisible para antivirus.

ThinkPwn / SMM vulnerabilities: Aplicado a Drivers de dispositivos. Bugs en el System Management Mode (SMM), un modo de CPU aún más privilegiado que el kernel. Explotar SMM permite escribir en la flash del firmware para lograr persistencia total. Sobrevive a reinstalaciones del OS y al reemplazo del disco.

---------------------------------------------------------------------------------
¿Qué es Converged Security and Management Engine (CSME), the Intel Management Engine BIOS Extension (Intel MEBx)?

CSME es un subsistema autónomo integrado en los chipsets Intel que funciona de manera completamente independiente al CPU principal. Cuenta con su propio procesador (ARC/x86 de 32 bits), su propia RAM, su propio sistema operativo; y acceso directo a la red, memoria y almacenamiento incluso con el equipo apagado,o mientras haya energía en standby. Lo clave del CSME es su posición en la jerarquía de privilegios: corre por debajo del sistema operativo, debajo del hypervisor y por debajo del SMM. Es el componente con mayor acceso al hardware. 

Por otro lado, Intel MEBx (Management Engine BIOS Extension) es la interfaz de configuración del CSME. Es una interfaz de texto que aparece durante el POST y permite configurar qué capacidades de AMT están habilitadas, con qué credenciales, y en qué red opera. Es accesible previo a la carga del SO. 


---------------------------------------------------------------------------------
¿Qué es coreboot? ¿Qué productos lo incorporan? ¿Cuáles son las ventajas de su utilización?

Coreboot es un firmware de código abierto que reemplaza al BIOS/UEFI propietario. Intenta hacer lo mínimo en firmware y delegar el resto a un payload. Es, escencialmente, un núcleo de arranque. 

Productos que lo incorporan: Google Chromebooks y ChromeOS Flex, System76, Framework Laptop y también servidores de Google. 

Algunas ventajas que presenta su utilización: 

1) Al ser código abierto cualquiera puede revisar qué hace exactamente el firmware, con UEFI propietario eso es imposible.

2) Coreboot hace sustancialmente menos cosas que un UEFI completo.

3) Sin el overhead de las fases SEC/PEI/DXE/BDS, coreboot puede entregar el control al SO en 1–3 segundos en lugar de los 20–60 habituales de un UEFI propietario.

---------------------------------------------------------------------------------

¿Qué es un linker? ¿qué hace?
¿Qué es la dirección que aparece en el script del linker?¿Por qué es necesaria?
Compare la salida de objdump con hd, verifique donde fue colocado el programa dentro de la imagen.
Grabar la imagen en un pendrive y probarla en una pc y subir una foto.
¿Para qué se utiliza la opción --oformat binary en el linker?

---

## Referencias
