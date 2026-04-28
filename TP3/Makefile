# Crea una imagen main.img booteable
compilar:
	@echo "Compilando imagen"
	@as -g -o main.o main.S
	@ld --oformat binary -o main.img -T link.ld main.o
	@echo "Imagen compilada"
	@echo "Compilando programa para testear error de escritura en segmento de solo lectura"
	@nasm -f bin segmentos_mal_configurados.asm -o test.bin
	@echo "Programa compilado"

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
	@sudo dd if=main.img of=/dev/$(NAME) bs=446 count=1 conv=notrunc

ejecutar_test: compilar
	@qemu-system-i386 -drive format=raw,file=test.bin -d int -no-reboot -s -S
