[org 0x7C00]
bits 16

start:
    cli

    ; Habilita A20
    in al, 0x92
    or al, 00000010b
    out 0x92, al

    ; Carga GDT 
    lgdt [gdt_descriptor]

    ; Activa modo protegido
    mov eax, cr0
    or eax, 1
    mov cr0, eax

    ; Salto largo
    jmp 0x08:protected_mode_entry

; -------------------------
; GDT
; -------------------------
gdt_start:

gdt_null:
    dq 0x0000000000000000

gdt_code:
    dq 0x00CF9A000000FFFF

gdt_data:
    dq 0x00CF92000000FFFF

gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

; -------------------------
; Modo protegido
; -------------------------

bits 32

protected_mode_entry:

    ; carga segmentos
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov fs, ax
    mov gs, ax

    ; stack simple
    mov esp, 0x90000

    ; loop infinito
hang:
    jmp hang

; -------------------------
; MBR signature
; -------------------------

times 510 - ($ - $$) db 0
dw 0xAA55