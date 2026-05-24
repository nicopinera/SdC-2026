[org 0x7C00]
bits 16

start:
    cli  ; Deshabilitar interrupciones

    ; Habilitar A20
    in al, 0x92
    or al, 00000010b
    out 0x92, al

    lgdt [gdt_descriptor]

    ; Activar modo protegido
    mov eax, cr0
    or eax, 1
    mov cr0, eax

    ; Far jump al selector 0x08 (Código)
    jmp 0x08:protected_mode_entry

; ────────────────────────────────────────────
; GDT - Definición Explícita de Descriptores
; ────────────────────────────────────────────
gdt_start:
    dq 0                        ; Descriptor Nulo obligatorio

; Selector 0x08: Segmento de Código
; Base: 0x00000000 | Límite: 0xFFFFF | G=1 (4KB), D=1 (32-bit) -> 4GB
gdt_code:
    dw 0xFFFF                   ; Límite [15:0]
    dw 0x0000                   ; Base [15:0]
    db 0x00                     ; Base [23:16]
    db 10011010b                ; Acceso: P=1, DPL=0, S=1, Tipo=Code(R/E)
    db 11001111b                ; Flags: G=1, D=1, L=0, AVL=0 | Límite [19:16]
    db 0x00                     ; Base [31:24]

; Selector 0x10: Segmento de Datos (BASE DIFERENCIADA)
; Base: 0x00020000 | Límite: 4GB
gdt_data:
    dw 0xFFFF                   ; Límite [15:0]
    dw 0x0000                   ; Base [15:0]
    db 0x02                     ; Base [23:16] -> 0x02 << 16 = 0x20000
    db 10010010b                ; Acceso: P=1, DPL=0, S=1, Tipo=Data(R/W)
    db 11001111b                ; Flags: G=1, D=1, L=0, AVL=0 | Límite [19:16]
    db 0x00                     ; Base [31:24]
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

; ─────────────────────────────────────────────────────────────────────
bits 32
protected_mode_entry:
    mov ax, 0x10                ; Cargar selector de datos (base 0x20000)
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov esp, 0x90000

    ; Escritura lógica en offset 0. 
    ; Dirección física resultante: 0x20000 + 0 = 0x20000
    mov dword [0], 0xCAFEBABE

hang:
    jmp hang

times 510 - ($ - $$) db 0
dw 0xAA55