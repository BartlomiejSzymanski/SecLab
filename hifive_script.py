import time
import pylink
import serial
import serial.tools.list_ports

BOARD_NAME = 'HiFive'
hifive_serial_no = ''
hifive_ports = []


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
    line = hifive_port_1.readline().decode('utf-8')
    print(line)
words = line.split(' ')
MAC_ADDR = words.pop()
print('MAC ADDRESS:', MAC_ADDR)
password = '__SecLab__' + MAC_ADDR
print('PASSWORD:', password)


hifive_port_0.flushInput()
time.sleep(3)
line = ''
while 'Welcome.' not in line:
    try:
        line = hifive_port_0.readline()
        time.sleep(0.1)
        print(line)
        line = line.decode('utf-8')
    except:
        print('KeyboardInterrupt')
        break



# time.sleep(0.1)
# hifive_port_0.write(b'__SecLab__3c:71:bf:b9:59:e0\r')
# time.sleep(0.1)

# while 'Falken' not in line:
#     line = hifive_port_0.readline().decode('utf-8')
#     print('line:',line)


# EPILOGUE
jlink.close()
hifive_port_0.close()
hifive_port_1.close()


# try:
#     result = subprocess.check_output("picocom -b 115200 /dev/ttyACM1", shell=True)
# except:
#     print('Dupa')











# print(ACM1_link.reset())




    # try:
    #     new_ports = serial.tools.list_ports.comports() - const_ports                        
    #     print(new_ports)
        
    #     # result = subprocess.check_output("ls /dev/ttyACM*", shell=True)
    #     break
    # except:
    #     print('No board connected')
        



# ACM0 = serial.Serial('/dev/ttyACM0', 115200)
# ACM1 = serial.Serial('/dev/ttyACM1', 115200)
# print(ACM1.port)
# os.system('ls /dev/ttyACM*')

# while os.system('ls /dev/tty*')               stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT

# while no new connection:
#    do nothing

# for i in range(2):
#   open new terminal
#   connect to dev/tty/ACM_ + i
#   var_console_out := capture terminal output // variable override in 2nd iter, will have the MAC addr inside
# // second terminal is the one printing mac adress
# var_MAC :=  scrape_MAC_addr(var_console_out
# password := form_password(var_MAC)
# input_password_to_ACM0()
