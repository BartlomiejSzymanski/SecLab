#include<stdio.h>
#include<stdint.h>
#define OUTPUT_ENABLE 0x08
#define OUTPUT_PORT   0x0C
#define IOF_EN        0x38
#define IOF_SEL       0x3C

#define GPIO_BASE     0x10012000

void main(void){

uint32_t *output_enable = (uint32_t *)(GPIO_BASE + OUTPUT_ENABLE);
uint32_t *output_port   = (uint32_t *)(GPIO_BASE + OUTPUT_PORT);
uint32_t *iof_en   = (uint32_t *)(GPIO_BASE + IOF_EN);
uint32_t *iof_sel   = (uint32_t *)(GPIO_BASE + IOF_SEL);

*output_enable = 0x01 << 21;
*output_port   = 0x01 << 21;
*iof_en        = 0x01 << 21;
*iof_sel       = 0x01 << 21;

}
