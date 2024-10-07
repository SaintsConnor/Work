.386  ; Specify instruction set
.model flat, stdcall  ; Flat memory model, std. calling convention
.stack 4096 ; Reserve stack space
ExitProcess PROTO, dwExitCode: DWORD  ; Exit process prototype
printf PROTO C :VARARG  ; Declare printf

.data ; data segment
    ; define your variables here
    answer DWORD ? ; Define answer variable
    format db "%d", 0 ; Format string for printing integers
  
.code ; code segment

PrintEAX PROC
    ; Save registers
    push ebp
    mov ebp, esp
    sub esp, 12
    pushad

    ; Print the value of EAX
    push eax
    push offset format
    call printf
    add esp, 8

    ; Restore registers
    popad
    mov esp, ebp
    pop ebp
    ret
PrintEAX ENDP

main PROC ; main procedure
    ; write your assembly code here
    mov eax, 10 ; Set EAX = 10
    mov ebx, 2 ; Set EBX = 2
    mov ecx, 4 ; Set ECX = 4
    mov edx, 9 ; Set EDX = 9

    add eax, ebx ; EAX = EAX + EBX
    add ecx, edx ; ECX = ECX + EDX

    sub eax, ecx ; EAX = EAX - ECX

    mov answer, eax ; Move EAX to answer variable

    ; display the answer
    call PrintEAX ; Call PrintEAX procedure

    INVOKE ExitProcess, 0 ; call exit function
  
main ENDP ; exit main procedure
END main  ; stop assembling
