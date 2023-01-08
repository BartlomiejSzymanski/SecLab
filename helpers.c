#include "helpers.h"
#include "syscalls.h"

void putchr(char chr) {
  uart0_putchr(chr);
}

unsigned int strlen(const char * str) {
  int len = 0;
  while (*str++) len++;
  return len;
}

void putstr(const char * str) {
  uart0_putstr_n(str, strlen(str));
}

void putuint(unsigned int val) {
  // fill buffer from the back
  char buffer[12];
  char * pos = buffer+11;
  *pos = 0; // null-termination

  // decode digits
  do {
    unsigned int digit = val % 10;
    val /= 10;
    *--pos = '0' + digit;
  } while (val);
  
  // print
  putstr(pos);
}

void putint(int val) {
  if (val < 0) {
    val = -val;
    putchr('-');
  }
  putuint((unsigned int) val);
}

char get_nibble_hex(unsigned int val) {
  val &= 0xf;               // mask to nibble
  if (val >= 10)
    return 'a' + val - 10;  // to alpha digit
  return '0' + val;         // to num digit
}

void puthex(unsigned int val) {
  char buffer[11] = "0x00000000";
  for (unsigned int pos = 9; pos > 1; pos--) {
    buffer[pos] = get_nibble_hex(val);
    val >>= 4;
  }
  uart0_putstr_n(buffer, 10);
}

// needed as builtin
void memcpy(char * dest, const char * src, unsigned int len) {
  for (; len > 0; len--)
    *dest++ = *src++;
}
