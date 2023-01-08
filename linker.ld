SECTIONS {

  /* ITIM memory */
  . = 0x8001000;

  .startup : {
    *(.startup)
  }

  .text : {
    *(.text*)
  }
  
  . = ALIGN(4);

  .rodata : { *(.rodata*) }

  /* DTIM memory */
  . = 0x80000000;

  .data (NOLOAD) : { *(.data*) }

  /* variables for bss initializations */
  . = ALIGN(4);
  __bss_start = .;
  .bss : { *(.bss*) }
  . = ALIGN(4);
  __bss_end = .;
}
