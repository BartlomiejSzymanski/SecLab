#include "syscalls.h"
#include "helpers.h"

void __attribute__((noreturn)) exit(int rc) {
  if (rc) {
    putstr("exitcode: ");
    putint(rc);
    putstr("\r\n");
  }
  register int syscall_nr asm("a0") = 1;
  asm volatile("ecall" :: "r"(syscall_nr));
  __builtin_unreachable();
}

void uart0_putchr(char c) {
  register int syscall_nr asm("a0") = 2;
  register int arg0 asm("a1") = (int) c;
  asm volatile("ecall" :: "r"(syscall_nr), "r"(arg0));
}

void uart0_putstr_n(const char * str, unsigned int len) {
  register int syscall_nr asm("a0") = 3;
  register int arg0 asm("a1") = (int) str;
  register int arg1 asm("a2") = len;
  asm volatile("ecall" :: "r"(syscall_nr), "r"(arg0), "r"(arg1));
}

char uart0_getchr() {
  register int syscall_nr_and_ret asm("a0") = 4;
  asm volatile("ecall" : "+r"(syscall_nr_and_ret));
  return (char) syscall_nr_and_ret;
}

void set_stack_size(unsigned int size) {
  register int syscall_nr asm("a0") = 5;
  register int arg0 asm("a1") = (int) size;
  asm volatile("ecall" :: "r"(syscall_nr), "r"(arg0));
}

void get_stack_bottom(unsigned int * bottom) {
  register int syscall_nr asm("a0") = 6;
  register int arg0 asm("a1") = (int) bottom;
  asm volatile("ecall" :: "r"(syscall_nr), "r"(arg0) : "memory");
}

void unlock_syscalls(unsigned int debug_token) {
  register int syscall_nr asm("a0") = 7;
  register int arg0 asm("a1") = (int) debug_token;
  asm volatile("ecall" :: "r"(syscall_nr), "r"(arg0));
}

