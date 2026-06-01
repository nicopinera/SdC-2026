# Trabajo práctico 5 - Device drivers

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

**Fecha:** 23/5/2026

---

## Información de los autores

- **Información de contacto**:
  - [nicolas.pinera@mi.unc.edu.ar](mailto:nicolas.pinera@mi.unc.edu.ar)
  - [julian.krede@mi.unc.edu.ar](mailto:julian.krede@mi.unc.edu.ar)
  - [juana.pucheta.noguera@mi.unc.edu.ar](mailto:juana.pucheta.noguera@mi.unc.edu.ar)

---

---

## Introducción
En este trabajo práctico se desarrolla el diseño y la construcción de un CDD (Character Device Driver) en una Raspberry Pi para implementar en Linux. El mismo tiene como función principal sensar dos señales con un periodo de 1 segundo y visualizar una de ellas, elegida por el usuario, en la pantalla del ordenador.

## Estructura del proyecto
## Flujo de trabajo
1. Escribir código en la PC host (VSCodium)
2. Cross-compilar con el Makefile apuntando a ARM
3. Transferir binarios a la Raspberry Pi via `scp`
4. Ejecutar y visualizar desde el navegador del host

## Requisitos del host
- Compilador cruzado: `arm-linux-gnueabihf-gcc` (o `aarch64` según el modelo)
- Headers del kernel de la Raspberry Pi (versión específica)
- `make`, `ssh`, `scp`

## Conclusión