.code16
.global _start

_start:
    ljmp $0, $real_start

real_start:
    # Inicializa registros de datos y stack
    xor %ax, %ax
    mov %ax, %ds
    mov %ax, %es
    mov %ax, %ss
    mov $0x7c00, %sp

    # Limpia la pantalla y establecer modo texto
    mov $0x0003, %ax
    int $0x10

    # Configura registros para imprimir
    mov $msg, %si
    mov $0x0e, %ah
    xor %bh, %bh     # PÁGINA DE VIDEO 0 (Crítico para hardware real)
    mov $0x07, %bl   # Gris claro sobre negro (esto es opcional, algunas BIOS lo requieren)

loop:
    lodsb
    or %al, %al
    jz halt
    int $0x10
    jmp loop

halt:
    hlt
    jmp halt

msg:
    .asciz "hello world from BIOS! we are Bare Metal Guys"