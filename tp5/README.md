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

**Fecha:** 10/6/2026

---

## Información de los autores

- **Información de contacto**:
  - [nicolas.pinera@mi.unc.edu.ar](mailto:nicolas.pinera@mi.unc.edu.ar)
  - [julian.krede@mi.unc.edu.ar](mailto:julian.krede@mi.unc.edu.ar)
  - [juana.pucheta.noguera@mi.unc.edu.ar](mailto:juana.pucheta.noguera@mi.unc.edu.ar)

---

## Introducción

En Linux, la comunicación entre el hardware y el software de usuario se realiza a través de **drivers** — módulos del kernel que abstraen el acceso a los dispositivos físicos y los exponen como archivos en el sistema de archivos. Los **Character Device Drivers (CDD)** son aquellos que permiten leer y escribir datos de forma secuencial, byte a byte, y son la base de la mayoría de los periféricos de entrada/salida en sistemas embebidos.

En este trabajo práctico se diseña e implementa un CDD para arquitectura ARM64, destinado a correr sobre una Raspberry Pi (o su equivalente emulado en QEMU). El driver expone el dispositivo `/dev/cdd`, que genera dos señales simuladas con un período de 1 segundo — temperatura y presión — y permite al usuario seleccionar cuál de ellas visualizar.

El desarrollo sigue el enfoque de **compilación cruzada**: todo el código se escribe y compila en la PC host (x86), y los binarios resultantes se transfieren a la plataforma ARM64 via SSH. Para el entorno de ejecución se utilizó **Buildroot** para generar un sistema Linux completo (kernel + rootfs) y **QEMU** para emularlo, lo que permitió desarrollar y validar el trabajo sin necesidad de hardware físico.

La visualización se resuelve con una interfaz web servida desde la VM: un servidor Python lee `/dev/cdd` y expone los datos por HTTP, permitiendo ver el gráfico de la señal en tiempo real desde el navegador del host.

## Estructura del trabajo practico

```
tp5/
├── driver/
│   ├── cdd.c          # Módulo del kernel (Character Device Driver)
│   └── Makefile       # Cross-compilación del módulo para ARM64
├── userapp/
│   ├── server.py      # Servidor HTTP que lee /dev/cdd y sirve la web
│   └── web/
│       └── index.html # Interfaz gráfica con Chart.js
├── makefile           # Targets de build, deploy, load y QEMU
├── Image              # Kernel Linux 6.1.44 ARM64 (generado con Buildroot)
└── rootfs.img         # Sistema de archivos raíz ARM64 (generado con Buildroot)
```

## Flujo de trabajo resumido

1. Obtener el sistema Linux completo para ARM64 con Buildroot
2. Escribir y cross-compilar el módulo del kernel (`cdd.ko`) en el host
3. Transferir los binarios a la máquina virtual via SSH
4. Cargar el módulo y ejecutar el servidor en la VM
5. Visualizar los datos desde el navegador del host

## Desarrollo

### Device Drivers

Un **device driver** es un módulo de software que forma parte del kernel y actúa como intermediario entre el hardware y los programas de usuario. Su función es abstraer los detalles del dispositivo físico y exponerlo a través de una interfaz estándar — en Linux, un archivo en `/dev/` — de forma que cualquier programa pueda interactuar con el hardware usando las syscalls comunes (`open`, `read`, `write`, `close`) sin necesidad de conocer cómo funciona internamente el dispositivo.

Linux clasifica los device drivers en dos tipos principales:

- **Character Device Driver (CDD)**: el acceso al dispositivo es secuencial, byte a byte, sin estructura de bloques. Es el modelo adecuado para periféricos de flujo continuo de datos: sensores, puertos serie, terminales. No tienen un sistema de archivos propio y no permiten `seek` arbitrario en la mayoría de los casos.

- **Block Device Driver (BDD)**: el acceso se realiza en bloques de tamaño fijo (típicamente 512 bytes o 4 KB). El kernel puede reordenar y cachear las operaciones para optimizar el rendimiento. Es el modelo usado por discos rígidos, SSDs y memorias flash.

Para este trabajo se implementó un CDD, ya que el dispositivo produce un flujo continuo de muestras que se consumen de a una lectura por vez, lo que se corresponde exactamente con el modelo de acceso secuencial.

### Obtención del sistema Linux con Buildroot

Dado que el trabajo se desarrolla sin hardware físico, se utilizó **QEMU** para emular un procesador ARM64 (Cortex-A72). Para esto se necesita tanto un kernel como un sistema de archivos raíz compatibles con esa arquitectura, los cuales se generaron con **Buildroot**.

Buildroot es una herramienta que automatiza la construcción de sistemas Linux embebidos completos: descarga, configura y compila el kernel, las bibliotecas y el userspace apuntando a la arquitectura destino, todo desde el host x86. El proceso que automatiza es el siguiente:

```
Código fuente
    ↓
Cross Compiler
    ↓
Kernel Linux
    ↓
Root Filesystem
    ↓
Imagen booteable
```

#### Pasos realizados

**1. Descarga y configuración inicial**

Se descargó Buildroot 2024.02 y se aplicó el defconfig para QEMU AArch64, que preconfigura el kernel y el toolchain para la máquina virtual `virt` de QEMU:

```bash
wget https://buildroot.org/downloads/buildroot-2024.02.tar.gz
tar xf buildroot-2024.02.tar.gz
cd buildroot-2024.02
make qemu_aarch64_virt_defconfig
```

**2. Configuración de paquetes adicionales**

Dentro del menú de configuración interactivo se agregaron las dependencias necesarias para el trabajo:

```bash
make menuconfig
```

Las opciones habilitadas fueron:

| Sección                                   | Opción                            | Motivo                                               |
| ----------------------------------------- | --------------------------------- | ---------------------------------------------------- |
| Target packages → Interpreter languages   | `python3`                         | Para ejecutar `server.py` en la VM                   |
| Target packages → Networking applications | `openssh`                         | Para transferir binarios y ejecutar comandos via SSH |
| System configuration                      | Root password                     | Para permitir login SSH como root                    |
| Filesystem images                         | `ext2/3/4 root filesystem (ext4)` | Para elFormato del rootfs para QEMU                  |

**3. Compilación**

```bash
make -j$(nproc)
```

El proceso tardó aproximadamente 30 minutos en la primera ejecución. Buildroot descarga los fuentes hace la cross-compilación para ARM64 y genera los artefactos finales en `output/images/`:

- `Image`: Kernel Linux 6.1.44 en formato binario para ARM64
- `rootfs.ext4`: Sistema de archivos raíz con Python 3, OpenSSH y utilidades base

Ambos archivos se copiaron a la raíz del proyecto y `rootfs.ext4` se renombró a `rootfs.img`.

**4. Ejecución**

Finalmente con todos los archivos necesarios corremos la VM en qemu mediante el siguiente comando:

```bash
qemu-system-aarch64 \
-M virt \
-cpu cortex-a72 \
-m 1024 \
-kernel Image \
-drive file=rootfs.img,format=raw \
-append "root=/dev/vda rw console=ttyAMA0" \
-netdev user,id=n1,hostfwd=tcp::$(PI_PORT)-:22,hostfwd=tcp::9090-:9090 \
-device virtio-net-pci,netdev=n1 \
-nographic
```

Y luego permitimos el acceso acceso a root con contraseña mediante:

```bash
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
/etc/init.d/S50sshd restart
```

![Linux ARM64 en qemu](https://github.com/user-attachments/assets/34650b6b-b902-4695-9884-576cf1bd587f)

#### Headers de kernel y compatibilidad de módulos

Existen dos tipos de headers del kernel con propósitos distintos. Los **headers de userspace** (UAPI) definen la interfaz entre programas y el kernel: syscalls, estructuras de `ioctl`, constantes. Son los que instala `apt` con `linux-headers-*` y los que usa cualquier programa de usuario.

Los **headers para módulos**, por otro parte, exponen las estructuras internas del kernel: `struct file_operations`, `struct cdev`, `spinlock_t`, etc. Para compilar un módulo no alcanza con esos headers, también se necesita el **kernel build tree** completo, que incluye el `.config` con el que se compiló el kernel, el `Module.symvers` con la tabla de símbolos exportados, y los scripts de build que generan el `.ko`.

Cuando el kernel carga un módulo, verifica una cadena llamada **vermagic** embebida en el `.ko`. Por ejemplo: 6.1.44 SMP preempt mod_unload aarch64

Esta cadena se construye a partir de la versión, flags de compilación y arquitectura. Si el módulo fue compilado contra un kernel build tree diferente al que está corriendo, el módulo es rechazado antes de ejecutar una sola línea de código.

En nuestro caso, Buildroot resuelve esto de forma natural: Al compilar el kernel desde cero, deja el árbol de fuentes completo en `output/build/linux-6.1.44/`. Ese mismo directorio se usa como `KERNEL_DIR` para cross-compilar `cdd.ko`, por lo que el módulo y el kernel que corre en QEMU comparten exactamente el mismo vermagic y la carga siempre es exitosa.

### Cross-compilación del módulo

Con el sistema generado, se cross-compiló el módulo del kernel desde el host x86 apuntando a ARM64:

```bash
# Instala el compilador cruzado
sudo apt install gcc-aarch64-linux-gnu

# Compila cdd.ko
make build KERNEL_DIR=<path>/buildroot-2024.02/output/build/linux-6.1.44
```

El resultado es `driver/cdd.ko`, un módulo ELF para ARM64 listo para ser cargado en la VM.

### El driver: cdd.c

El módulo del kernel implementa un Character Device Driver que expone el archivo de dispositivo `/dev/cdd`. Al cargarse, registra el dispositivo en el sistema y lanza un kernel timer que genera un nuevo valor de señal cada segundo. Al descargarse, cancela el timer y libera todos los recursos.

#### Registro del dispositivo

El driver usa la API moderna de character devices del kernel:

1. `alloc_chrdev_region`: solicita al kernel un número mayor dinámico (no se hardcodea ningún número para evitar conflictos)
2. `cdev_init` + `cdev_add`: registra el dispositivo con sus file operations
3. `class_create` + `device_create`: crea la clase y el nodo en `/dev/cdd` automáticamente via udev, sin necesidad de `mknod` manual

#### Generación de señales con kernel timer

El driver utiliza un `struct timer_list` para actualizar el valor medido cada segundo (`HZ` jiffies). En cada disparo se genera un número aleatorio con `get_random_bytes` y se calcula el valor de la señal activa:

- **Señal 1 — Temperatura**: valor en el rango 20–35 °C
- **Señal 2 — Presión**: valor en el rango 950–1050 hPa

El acceso a las variables compartidas entre el timer y las file operations está protegido con un `spinlock`, ya que el timer corre en contexto de interrupción.

#### Operaciones del dispositivo

**`read`** — devuelve el valor actual de la señal activa como string ASCII seguido de `\n`. El offset se actualiza para que lecturas sucesivas dentro del mismo `open()` devuelvan EOF, lo que permite que la aplicación de usuario lea con un simple `open/read/close` en cada muestra.

**`write`** — recibe el carácter `"1"` o `"2"` y cambia la señal activa. Se descarta cualquier whitespace o newline al final para compatibilidad con `echo`.

### Conexión SSH a la VM

Una vez que QEMU arranca, la VM queda accesible desde el host a través del port forwarding configurado en el makefile (puerto 2222 del host mapeado al puerto 22 de la VM):

```bash
ssh -p 2222 root@localhost
```

![Conexion ssh exitosa](https://github.com/user-attachments/assets/6712b2d1-c3a0-44de-827b-78e9e95c237c)

### Transferencia de archivos mediante la conexion SSH usando SCP

Para traspasar el modulo cross-compilado, el programa del servidor y la pagina desde el host a la VM usamos SCP

![Archivos transferidos](https://github.com/user-attachments/assets/1b51fbd6-c4cf-40e4-9f4c-d55aa79fd0fc)

### Carga del módulo

Con los binarios ya transferidos via `make deploy`, se carga el módulo desde la VM:

```bash
insmod cdd.ko
dmesg | tail -3
ls -l /dev/cdd
```

![Carga exitosa de modulo](https://github.com/user-attachments/assets/afc40959-39e2-41dd-b241-ad91730b60f5)

### Descarga del modulo

Finalmente para descargar el módulo (al finalizar el trabajo):

```bash
sudo rmmod cdd
dmesg | tail -2
```

![Modulo descargado](https://github.com/user-attachments/assets/86dd75a3-2d16-4e6c-9ab8-e6f7e3be99cd)

---

### Aplicación de usuario y visualización web

La capa de usuario está compuesta por dos partes: un servidor HTTP escrito en Python y una página web que grafica los datos en tiempo real.

#### server.py

El servidor actúa como puente entre `/dev/cdd` y el navegador. Corre en el puerto 9090 dentro de la VM y expone tres endpoints:

| Endpoint               | Descripción                                                                                          |
| ---------------------- | ---------------------------------------------------------------------------------------------------- |
| `GET /`                | Sirve la página `index.html`                                                                         |
| `GET /data`            | Lee `/dev/cdd`, agrega el valor al historial (últimos 60 puntos) y devuelve un JSON `{signal, data}` |
| `GET /select?signal=N` | Escribe `N` en `/dev/cdd` para cambiar la señal activa y resetea el historial                        |

Cada vez que `/data` es consultado, el servidor reabre `/dev/cdd` desde cero — esto es correcto para un character device, ya que cada `open()` resetea el offset y devuelve el valor más reciente.

El servidor tiene un flag `USE_DEVICE` en la parte superior del archivo:

- `True` → lee y escribe sobre `/dev/cdd` (driver real cargado)
- `False` → usa los archivos `/tmp/cdd_value` y `/tmp/cdd_signal` generados por `simulador_cdd.sh` (útil para desarrollo sin la VM)

#### Interfaz web (index.html)

La página web usa **Chart.js** para graficar la señal en tiempo real. Se ejecuta en el navegador del host y se comunica con el servidor que corre dentro de la VM.

Cada segundo, el JavaScript hace un `fetch('/data')` al servidor, actualiza el gráfico con el nuevo punto y muestra la unidad de medición correspondiente a la señal activa. El usuario puede cambiar entre señales con los botones, lo que resetea el gráfico y envía el comando de selección al driver a través del servidor.

![Presion](https://github.com/user-attachments/assets/84dd2544-557e-4b10-a276-9408098e8724)

![Temperatura](https://github.com/user-attachments/assets/8cfd0e04-8f1d-4a27-bedb-c90f6d242e2a)

Finalmente apagamos el servidor, removemos el modulo (se muestra en "Descarga del modulo") y apagamos la maquina virtual

---

## Despliegue y ejecución

Para simplificar la ejecucion de comandos implementamos un makefile para simplificar las pruebas

En la terminal 1: Levantar la VM

```bash
make qemu

```

En la terminal 2: conexion ssh, transferencia de binario y encendido del servidor

```bash
make deploy
make load
make run
```

Una vez corriendo, la interfaz web queda disponible en `http://localhost:9090` desde el navegador del host.

## Conclusión

A lo largo del trabajo se implementó un sistema completo que abarca desde el desarrollo de un módulo del kernel hasta la visualización de datos en un navegador, pasando por cross-compilación, emulación de hardware y comunicación en red.

El principal desafío fue comprender y respetar las restricciones del entorno embebido: la necesidad de que los headers del kernel coincidan exactamente con el kernel en ejecución (vermagic), el manejo de concurrencia entre el kernel timer y las file operations mediante spinlocks, y la configuración del entorno QEMU con port forwarding para hacer accesibles los servicios desde el host.

Buildroot demostró ser una herramienta clave: al generar tanto el sistema que corre en QEMU como el árbol de fuentes del kernel usado para compilar el módulo, elimina por diseño el problema de incompatibilidad de versiones que es una fuente frecuente de errores en el desarrollo de drivers.

El resultado es un flujo de trabajo reproducible — desde `make build` hasta ver el gráfico en el navegador — que refleja fielmente el proceso que se aplicaría con hardware real: cross-compilar en el host, transferir via SSH y cargar el módulo en la plataforma destino.
