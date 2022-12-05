#game_binary: game.o
#	objcopy -j .text -O binary -I elf32-big game.o game_binary

#game.o: game.c
#	riscv64-unknown-elf-gcc -o game.o -march=rv32imac -mabi=ilp32 -mbig-endian -c game.c


all: custom_game1.bin custom_game2.bin

custom_game1.bin: custom_game1.o
	objcopy -j .text -O binary -I elf32-big custom_game1.o custom_game1.bin

custom_game1.o: custom_game1.s
	riscv64-linux-gnu-as -march=rv32ima -mabi=ilp32 -mbig-endian -o custom_game1.o custom_game1.s

custom_game2.bin: custom_game2.o
	objcopy -j .text -O binary -I elf32-big custom_game2.o custom_game2.bin

custom_game2.o: custom_game2.s
	riscv64-linux-gnu-as -march=rv32ima -mabi=ilp32 -mbig-endian -o custom_game2.o custom_game2.s
clean:
	rm -f custom_game1.o  custom_game1.bin custom_game2.o custom_game2.bin


