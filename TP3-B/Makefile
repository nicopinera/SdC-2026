install_dependencies:
	@sudo apt update
	@sudo apt install -y \
		qemu-system-x86 \
		ovmf \
		gnu-efi \
		build-essential \
		binutils-mingw-w64 \
		ghidra

create_img:
	dd if=/dev/zero of=disk.img bs=1M count=64
	mkfs.vfat -F 32 disk.img

init_qemu: create_img
	qemu-system-x86_64 -m 512 -bios /usr/share/ovmf/OVMF.fd -drive format=raw,file=disk.img -net none


compilacion:
	@echo "Iniciando compilacion"
	@gcc -I/usr/include/efi -I/usr/include/efi/x86_64 -I/usr/include/efi/protocol \
	-fpic -ffreestanding -fno-stack-protector -fno-strict-aliasing \
	-fshort-wchar -mno-red-zone -Wall -c -o aplicacion.o src/aplicacion.c

linkeo:
	@ld -entry _start -shared -Bsymbolic -L/usr/lib -L/usr/lib/efi -T /usr/lib/elf_x86_64_efi.lds \
	/usr/lib/crt0-efi-x86_64.o aplicacion.o -o aplicacion.so -lefi -lgnuefi

ejecutable:
	@objcopy -j .text -j .sdata -j .data -j .dynamic -j .dynsym -j .rel -j .rela -j .rel.* -j .rela.* -j .reloc \
	--target=efi-app-x86_64 aplicacion.so aplicacion.efi

programa: compilacion linkeo ejecutable
	@echo "Programa compilado"

.PHONY: clean

clean: 
	rm aplicacion.so aplicacion.o
