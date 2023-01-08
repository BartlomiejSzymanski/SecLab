#include "syscalls.h"
#include "helpers.h"


int main(void){
    uart0_putstr_n((char*)0x800039a4, 4);
    exit(0);
    
    return 0;
}