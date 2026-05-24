[org 0x7C00]
bits 16

start:
    cli
    in al, 0x92
    or al, 00000010b
    out 0x92, al

    lgdt [gdt_descriptor]

    mov eax, cr0
    or eax, 1
    mov cr0, eax

    jmp 0x08:protected_mode_entry

; ───────────────────────────────────
; GDT - Configuración de Protección
; ───────────────────────────────────
gdt_start:
    dq 0

; Selector 0x08: Código (Normal)
gdt_code:
    dw 0xFFFF           ; Límite [15:0]
    dw 0x0000           ; Base [15:0]
    db 0x00             ; Base [23:16]
    db 10011010b        ; Atributos
    db 11001111b        ; Flags
    db 0x00             ; Base [31:24]

; Selector 0x10: Datos de solo lectura
gdt_data_ro:
    dw 0xFFFF                   ; Límite [15:0]
    dw 0x0000                   ; Base [15:0]
    db 0x00                     ; Base [23:16]
    db 10010000b                ; Atributos, aca Bit Writable = 0 (Solo Lectura)
    db 11001111b                ; Flags
    db 0x00                     ; Base [31:24]
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

bits 32
protected_mode_entry:
    mov ax, 0x10                ; Cargar el selector Read-Only
    mov ds, ax
    mov ss, ax
    mov esp, 0x90000

    ; Al intentar escribir provoca Excepción #GP (General Protection Fault)
    mov dword [0x500], 0xDEADBEEF 

hang:
    jmp hang

times 510 - ($ - $$) db 0
dw 0xAA55