#include "syscalls.h"

extern unsigned int __bss_start;
extern unsigned int __bss_end;

int main();

void __attribute__((naked, section (".startup"), noreturn)) _start() {

  for (unsigned int * bss = &__bss_start; bss < &__bss_end; bss++)
    *bss = 0;

  int rc = main();

  exit(rc);

  __builtin_unreachable();
}

