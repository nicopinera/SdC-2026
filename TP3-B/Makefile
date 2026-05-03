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

compilar:
	cmake -S . -B build
	cmake --build build
