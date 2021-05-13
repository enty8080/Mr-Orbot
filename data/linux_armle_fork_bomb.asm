section .text
global _start

_start:
    BITS 32
    add r3, PC, #1
    bx r3

    BITS 16

_loop:
    eor r7, r7
    mov r7, #2
    svc #1
    mov r8, r8
    bl _loop
