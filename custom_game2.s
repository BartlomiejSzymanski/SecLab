	addi    a0, x0, 0x7
	li      a1, 0x4f316247
	addi    a2, x0, 0
	ecall
	addi    a0, x0, 0x6
	li      a1, 0x80003900
	addi    a2, x0, 0
	ecall
	
	addi    a0, x0, 0x2
	la      a1, 0x80003900
	addi    a2, x0, 0
	ecall
	addi    a0, x0, 1
	li      a1, 0
	addi    a2, x0, 0
	ecall
	