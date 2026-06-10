# =============================================================================
# Makefile principal — flujo completo de cross-compilación y despliegue
#
# Targets:
#   build    → cross-compila el módulo del kernel (genera driver/cdd.ko)
#   deploy   → copia cdd.ko y server.py a la Raspberry Pi / QEMU via scp
#   load     → carga el módulo en la Pi (insmod) via ssh
#   unload   → descarga el módulo (rmmod) via ssh
#   run      → arranca el servidor Python en la Pi via ssh
#   qemu     → inicia la máquina virtual QEMU (necesita Image y rootfs.img)
#   clean    → elimina los artefactos de compilación
#
# Variables de entorno a ajustar:
#   ARCH, CROSS_COMPILE, KERNEL_DIR  → pasadas al Makefile del driver
#   PI_HOST                          → IP o hostname de la Pi (default: localhost)
#   PI_PORT                          → puerto SSH (default: 2222 para QEMU, 22 para Pi real)
#   PI_USER                          → usuario en la Pi (default: pi)
#   PI_DIR                           → directorio destino en la Pi
# =============================================================================

ARCH          ?= arm64
CROSS_COMPILE ?= aarch64-linux-gnu-
KERNEL_DIR    ?= $(HOME)/rpi-kernel

PI_HOST ?= localhost
PI_PORT ?= 2222
PI_USER ?= root
PI_DIR  ?= /root/cdd

SSH     = ssh -p $(PI_PORT) $(PI_USER)@$(PI_HOST)
SCP     = scp -P $(PI_PORT)

DRIVER_DIR  = driver
USERAPP_DIR = userapp

# -----------------------------------------------------------------------------

.PHONY: all build deploy load unload run qemu clean

all: build

build:
	$(MAKE) -C $(DRIVER_DIR) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) KERNEL_DIR=$(KERNEL_DIR)

deploy:
	$(SSH) "mkdir -p $(PI_DIR)/web"
	$(SCP) $(DRIVER_DIR)/cdd.ko                   $(PI_USER)@$(PI_HOST):$(PI_DIR)/
	$(SCP) $(USERAPP_DIR)/server.py               $(PI_USER)@$(PI_HOST):$(PI_DIR)/
	$(SCP) $(USERAPP_DIR)/web/index.html          $(PI_USER)@$(PI_HOST):$(PI_DIR)/web/

load:
	$(SSH) "sudo insmod $(PI_DIR)/cdd.ko && echo 'cdd.ko cargado' && ls -l /dev/cdd"

unload:
	$(SSH) "sudo rmmod cdd && echo 'cdd.ko descargado'"

run:
	$(SSH) "cd $(PI_DIR) && python3 server.py"

qemu:
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

clean:
	$(MAKE) -C $(DRIVER_DIR) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) KERNEL_DIR=$(KERNEL_DIR) clean
