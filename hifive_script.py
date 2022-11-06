import time
import pylink
import serial
import serial.tools.list_ports
import threading

BOARD_NAME = 'HiFive'
hifive_serial_no = ''
hifive_ports = []

def read_from_port(port):
    line = ''
    for i in range(10):
        line = port.readline().decode('utf-8')
        print(line)
    
        
print('Waiting for board \n')
while(len(hifive_ports) <= 1):
    time.sleep(1)
    ports = serial.tools.list_ports.comports()
    for port in sorted(ports):
        if port.product == BOARD_NAME:
            hifive_serial_no = port.serial_number
            hifive_ports.append(port.device)      

print('Detected board at ports:',hifive_ports, '\nSERIAL_NO:  ', hifive_serial_no) 

jlink = pylink.JLink(serial_no= hifive_serial_no)
jlink.open()
jlink.connect(chip_name='RISC-V')
jlink.reset()


try:
    hifive_port_0 = serial.Serial(port= hifive_ports[0], baudrate= 115200) 
    hifive_port_1= serial.Serial(port= hifive_ports[1], baudrate= 115200)
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
print(mac_addr)

print(repr(mac_addr))
print(mac_addr.encode())

password= f'__SecLab__{mac_addr}'
password = password.encode()
print(password)

port_0_thread = threading.Thread(read_from_port(hifive_port_0))
port_0_thread.start()


hifive_port_0.write(password)

# EPILOGUE
jlink.close()
hifive_port_0.close()
hifive_port_1.close()

