SOURCE = src
DATA = data

compilar_y_ejecutar:
	gcc -Wall -pg $(SOURCE)/test_gprof.c $(SOURCE)/test_gprof_new.c -o test_gprof;\
	./test_gprof ;\
	gprof test_gprof gmon.out > $(DATA)/analisis.txt