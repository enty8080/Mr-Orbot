section .text
global _start

_start:
    xor rax, rax
    add rax, 57
    syscall
    jmp _start
