#include<string.h>
#include"syscalls.h"

typedef int (*callATCommand_t)(char[8], int, void*, int*, int*);
callATCommand_t callATCommand = (callATCommand_t) 0x20000208;


void main(void){
// function callATCommand in memory 0x20000208
//callATCommand("AT+RST",0,0,0,0);
//void *memcpy(void *dest, const void * src, size_t n)


memcpy((int*) 0x0800000, (int*)(int*) 0x08, 8192);

memcpy((int*) 0x0800000, (int*)callATCommand("AT+RST",0,0,0,0), 32);

uart0_putchr('a');

}