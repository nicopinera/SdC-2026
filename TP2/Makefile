instalar_dep:
	sudo apt install build-essential nasm gcc-multilib g++-multilib
	sudo apt install python3-dotenv

compilar:
	@echo "Compilando el programa"
	@nasm -f elf64 -g src/func_asm.asm -o func_asm.o # Compila el programa en assembler a binario
	@gcc -fPIC -c src/libpython.c -o libpython.o
	@gcc -shared func_asm.o libpython.o -o libpython.so
	@echo "Programa compilado"
