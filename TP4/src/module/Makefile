obj-m +=  mimodulo.o

.PHONY: generate_key sign_module registry_cert

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

compare:
	@awk '{print $$1}' lsmod_julian.txt | tail -n +2 | sort > mods_julian.txt
	@awk '{print $$1}' lsmod_nico.txt | tail -n +2 | sort > mods_nico.txt
	@awk '{print $$1}' lsmod_juana.txt | tail -n +2 | sort > mods_juana.txt
	@echo "Diferencias entre Nico y Julian" >> reporte.txt
	- diff mods_julian.txt mods_nico.txt >> reporte.txt
	@echo "Diferencias entre Julian y Juana" >> reporte.txt
	- diff mods_julian.txt mods_juana.txt  >> reporte.txt
	@echo "Diferencias entre Nico y Juana"  >> reporte.txt
	- diff mods_nico.txt mods_juana.txt  >> reporte.txt
	@rm mods_julian.txt mods_juana.txt mods_nico.txt

generate_key:
	@openssl req -new -x509 -newkey rsa:2048 \
	-keyout MOK.priv \
	-outform DER \
	-out MOK.der \
	-nodes \
	-days 36500 \
	-subj "/CN=BareMetalGuys/"

sign_module: generate_key
	/usr/src/linux-headers-$(shell uname -r)/scripts/sign-file \
	sha256 \
	MOK.priv \
	MOK.der \
	mimodulo.ko

register_cert:
	@sudo mokutil --import MOK.der