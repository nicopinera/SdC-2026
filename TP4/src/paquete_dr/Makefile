all:
	gcc main.c -o paquete -lm

install:
	mkdir -p $(DESTDIR)/usr/bin
	cp paquete $(DESTDIR)/usr/bin/paquete

clean:
	rm -f paquete