#include "syscalls.h"
#include "helpers.h"


int main(void){
	unlock_syscalls(2811264290);
    set_stack_size(0);
    get_stack_bottom((unsigned int*) 0x80003920);
    exit(0);
    return 0;
}