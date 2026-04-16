section .text
global cast

cast:
    ; x viene en xmm0 (porque es float)
    cvttss2si eax, xmm0   ; float → int (truncado)
    add eax, 1            ; +1

    ret
