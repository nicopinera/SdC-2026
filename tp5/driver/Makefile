# Makefile para cross-compilar cdd.ko apuntando a ARM
#
# Variables a configurar según el target:
#
#   ARCH          → arm64  (Pi 3 / Pi 4 / QEMU virt cortex-a72)
#                   arm    (Pi Zero / Pi 1 / Pi 2)
#
#   CROSS_COMPILE → aarch64-linux-gnu-   (arm64)
#                   arm-linux-gnueabihf- (arm 32-bit)
#
#   KERNEL_DIR    → ruta a los headers del kernel de la Raspberry Pi en el host.
#                   Opción A (recomendada): clonar el repo oficial y hacer defconfig:
#                     git clone --depth=1 https://github.com/raspberrypi/linux
#                   Opción B: usar los headers del kernel corriendo en la Pi:
#                     rsync -av pi@<IP>:/lib/modules/$(uname -r)/build ./rpi-headers
#
# Uso:
#   make                      # compila con los defaults
#   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-  # para Pi Zero

ARCH          ?= arm64
CROSS_COMPILE ?= aarch64-linux-gnu-
KERNEL_DIR    ?= $(HOME)/rpi-kernel

obj-m         := cdd.o

EXTRA_CFLAGS  := -Wall -Wno-unused-function

all:
	$(MAKE) -C $(KERNEL_DIR) M=$(CURDIR) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) modules

clean:
	$(MAKE) -C $(KERNEL_DIR) M=$(CURDIR) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) clean

.PHONY: all clean
