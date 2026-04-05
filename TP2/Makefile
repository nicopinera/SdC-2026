instalar_dep:
	sudo apt install build-essential nasm gcc-multilib g++-multilib

compilar:
	gcc -c -fPIC interface.c -o interface.o
	gcc -shared  interface.o -o libinterface.so