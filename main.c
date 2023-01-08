#include "syscalls.h"
#include "helpers.h"

volatile char target[4];
volatile unsigned int value = 0;

unsigned int getuint() {
  unsigned int value = 0;
  for (int i = 0; i < 4; i++) {
    value >>= 8;
    value |= ((unsigned int) uart0_getchr()) << 24;
  }
  return value;
}

int main() {

  target[0] = 'e';
  target[1] = 'x';
  target[2] = 'i';
  target[3] = 't';

  putstr("guess 4-byte value: ");
  value = getuint();
  putstr("\r\n");

  putstr("you entered: ");
  puthex(value);
  putstr("\r\n");

  if (value == *(unsigned int*) target) {
    putstr("Correct!\r\n");
    putstr("Bye\r\n");
    return 0;
  }

  putstr("Wrong!\r\n");
  putstr("Bye\r\n");

  return -1;
}

