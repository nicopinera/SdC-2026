# Crea una imagen main.img booteable
compilar:
	@echo "Compilando imagen"
	@as -g -o main.o main.S
	@ld --oformat binary -o main.img -T link.ld main.o
	@echo "Imagen compilada"

ejecutar_qemu: compilar
	@echo "Ejecutando la imagen en qemu"
	@qemu-system-x86_64 -hda main.img
	@echo "Ejecucion completada"

check-name:
ifndef NAME
	$(error ERROR: Usa lsblk para obtener el nombre del pendrive en el sistema, por ejemplo: sda, sdb, sdc. Luego: make grabar_pendrive NAME=sda )
	$(info ADVERTENCIA: COLOCAR MAL EL VALOR DE NAME PODRIA CORROMPER TU SISTEMA VERIFICA EL NOMBRE)
endif

grabar_pendrive: compilar check-name
	@sudo dd if=main.img of=/dev/$(NAME) bs=512 count=1 conv=fsync
