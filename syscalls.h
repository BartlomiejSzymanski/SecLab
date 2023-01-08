#ifndef __SYSCALLS_H__
#define __SYSCALLS_H__

void exit(int rc);

void uart0_putchr(char c);

void uart0_putstr_n(const char * str, unsigned int len);

char uart0_getchr();

void set_stack_size(unsigned int size);

void get_stack_bottom(unsigned int * bottom);

void unlock_syscalls(unsigned int debug_token);

#endif /* __SYSCALLS_H__ */
