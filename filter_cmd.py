import re

output= """\"AT",0,0,0,1\r\n\x00+CMD:1,"ATE0",0,0,0,1\r+CMD:2,"ATE1",0,0,0,1\r+CMD:3,"AT+RST",0,0,0,+CMD:4,"AT+GMR",0,0,0,+CMD:5,"AT+CMD",0,1,0,+CMD:6,"AT+GSLP",0,0,1+CMD:7,"AT+SYSTIMESTAM+CMD:8,"AT+SLEEP",0,1,+CMD:9,"AT+RESTORE",0,+CMD:10,"AT+SYSRAM",0,+CMD:11,"AT+SYSFLASH",+CMD:12,"AT+RFPOWER",0+CMD:13,"AT+SYSMSG",0,+CMD:14,"AT+SYSROLLBAC+CMD:15,"AT+SYSLOG",0,+CMD:16,"AT+SYSLSPCFG"+CMD:17,"AT+SYSLSP",0,+CMD:18,"AT+SYSSTORE",+CMD:19,"AT+SLEEPWKCFG+CMD:20,"AT+SYSREG",0,+CMD:21,"AT+USERRAM",0+CMD:22,"AT+CWMODE",0,+CMD:23,"AT+CWSTATE",0+CMD:24,"AT+CWJAP",0,1+CMD:25,"AT+CWRECONNCF+CMD:26,"AT+CWLAP",0,0+CMD:27,"AT+CWLAPOPT",+CMD:28,"AT+CWQAP",0,0+CMD:29,"AT+CWSAP",0,1+CMD:30,"AT+CWLIF",0,0+CMD:31,"AT+CWQIF",0,0+CMD:32,"AT+CWDHCP",0,+CMD:33,"AT+CWDHCPS",0+CMD:34,"AT+CWSTAPROTO+CMD:35,"AT+CWAPPROTO"+CMD:36,"AT+CWAUTOCONN+CMD:37,"AT+CWHOSTNAME+CMD:38,"AT+CWCOUNTRY"+CMD:39,"AT+CIFSR",0,0+CMD:40,"AT+CIPSTAMAC"+CMD:41,"AT+CIPAPMAC",+CMD:42,"AT+CIPSTA",0,+CMD:43,"AT+CIPAP",0,1+CMD:44,"AT+CIPV6",0,1+CMD:45,"AT+CIPDNS",0,+CMD:46,"AT+CIPDOMAIN"+CMD:47,"AT+CIPSTATUS"+CMD:48,"AT+CIPSTART",+CMD:49,"AT+CIPSTARTEX+CMD:50,"AT+CIPTCPOPT"+CMD:51,"AT+CIPCLOSE",+CMD:52,"AT+CIPSEND",0+CMD:53,"AT+CIPSENDEX"+CMD:54,"AT+CIPDINFO",+CMD:55,"AT+CIPMUX",0,+CMD:56,"AT+CIPRECVMOD+CMD:57,"AT+CIPRECVDAT+CMD:58,"AT+CIPRECVLEN+CMD:59,"AT+CIPSERVER"+CMD:60,"AT+CIPSERVERM+CMD:61,"AT+CIPSSLCCON+CMD:62,"AT+CIPSSLCCN"+CMD:63,"AT+CIPSSLCSNI+CMD:64,"AT+CIPSSLCALP+CMD:65,"AT+CIPSSLCPSK+CMD:66,"AT+CIPMODE",0+CMD:67,"AT+CIPSTO",0,+CMD:68,"AT+SAVETRANSL+CMD:69,"AT+CIPSNTPCFG+CMD:70,"AT+CIPSNTPTIM+CMD:71,"AT+CIPRECONNI+CMD:72,"AT+SECLAB",0,+CMD:73,"AT+DBG_TOKEN\""""

standard_commands= """AT: Test AT startup.
AT+RST: Restart a module.
AT+GMR: Check version information.
AT+CMD: List all AT commands and types supported in current firmware.
AT+GSLP: Enter Deep-sleep mode.
ATE: Configure AT commands echoing.
AT+RESTORE: Restore factory default settings of the module.
AT+UART_CUR: Current UART configuration, not saved in flash.
AT+UART_DEF: Default UART configuration, saved in flash.
AT+SLEEP: Set the sleep mode.
AT+SYSRAM: Query current remaining heap size and minimum heap size.
AT+SYSMSG: Query/Set System Prompt Information.
AT+USERRAM: Operate user’s free RAM.
AT+SYSFLASH: Query/Set User Partitions in Flash.
[ESP32 Only] AT+FS: Filesystem Operations.
AT+RFPOWER: Query/Set RF TX Power.
AT+SYSROLLBACK: Roll back to the previous firmware.
AT+SYSTIMESTAMP: Query/Set local time stamp.
AT+SYSLOG: Enable or disable the AT error code prompt.
AT+SLEEPWKCFG: Query/Set the light-sleep wakeup source and awake GPIO.
AT+SYSSTORE: Query/Set parameter store mode.
AT+SYSREG: Read/write the register.AT+CWMODE: Set the Wi-Fi mode (Station/SoftAP/Station+SoftAP).
AT+CWSTATE: Query the Wi-Fi state and Wi-Fi information.
AT+CWJAP: Connect to an AP.
AT+CWRECONNCFG: Query/Set the Wi-Fi reconnecting configuration.
AT+CWLAPOPT: Set the configuration for the command AT+CWLAP.
AT+CWLAP: List available APs.
AT+CWQAP: Disconnect from an AP.
AT+CWSAP: Query/Set the configuration of an ESP32 SoftAP.
AT+CWLIF: Obtain IP address of the station that connects to an ESP32 SoftAP.
AT+CWQIF: Disconnect stations from an ESP32 SoftAP.
AT+CWDHCP: Enable/disable DHCP.
AT+CWDHCPS: Query/Set the IPv4 addresses allocated by an ESP32 SoftAP DHCP server.
AT+CWAUTOCONN: Connect to an AP automatically when powered on.
AT+CWAPPROTO: Query/Set the 802.11 b/g/n protocol standard of SoftAP mode.
AT+CWSTAPROTO: Query/Set the 802.11 b/g/n protocol standard of station mode.
AT+CIPSTAMAC: Query/Set the MAC address of an ESP32 station.
AT+CIPAPMAC: Query/Set the MAC address of an ESP32 SoftAP.
AT+CIPSTA: Query/Set the IP address of an ESP32 station.
AT+CIPAP: Query/Set the IP address of an ESP32 SoftAP.
AT+CWSTARTSMART: Start SmartConfig.
AT+CWSTOPSMART: Stop SmartConfig.
AT+WPS: Enable the WPS function.
AT+MDNS: Configure the mDNS function.
AT+CWJEAP: Connect to a WPA2 Enterprise AP.
AT+CWHOSTNAME: Query/Set the host name of an ESP32 station.
AT+CWCOUNTRY: Query/Set the Wi-Fi Country Code.AT+CIPV6: Enable/disable the network of Internet Protocol Version 6 (IPv6).
AT+CIPSTATE: Obtain the TCP/UDP/SSL connection information.
AT+CIPSTATUS (deprecated): Obtain the TCP/UDP/SSL connection status and information.
AT+CIPDOMAIN: Resolve a Domain Name.
AT+CIPSTART: Establish TCP connection, UDP transmission, or SSL connection.
AT+CIPSTARTEX: Establish TCP connection, UDP transmission, or SSL connection with an automatically assigned ID.
[Data Mode Only] +++: Exit from the data mode.
AT+CIPSEND: Send data in the normal transmission mode or Wi-Fi normal transmission mode.
AT+CIPSENDL: Send long data in paraller in the normal transmission mode.
AT+CIPSENDLCFG: Set the configuration for the command AT+CIPSENDL.
AT+CIPSENDEX: Send data in the normal transmission mode in expanded ways.
AT+CIPCLOSE: Close TCP/UDP/SSL connection.
AT+CIFSR: Obtain the local IP address and MAC address.
AT+CIPMUX: Enable/disable the multiple connections mode.
AT+CIPSERVER: Delete/create a TCP/SSL server.
AT+CIPSERVERMAXCONN: Query/Set the maximum connections allowed by a server.
AT+CIPMODE: Query/Set the transmission mode.
AT+SAVETRANSLINK: Set whether to enter Wi-Fi normal transmission mode on power-up.
AT+CIPSTO: Query/Set the local TCP Server Timeout.
AT+CIPSNTPCFG: Query/Set the time zone and SNTP server.
AT+CIPSNTPTIME: Query the SNTP time.
AT+CIPSNTPINTV: Query/Set the SNTP time synchronization interval.
AT+CIPFWVER: Query the existing AT firmware version on the server.
AT+CIUPDATE: Upgrade the firmware through Wi-Fi.
AT+CIPDINFO: Set “+IPD” message mode.
AT+CIPSSLCCONF: Query/Set SSL clients.
AT+CIPSSLCCN: Query/Set the Common Name of the SSL client.
AT+CIPSSLCSNI: Query/Set SSL client Server Name Indication (SNI).
AT+CIPSSLCALPN: Query/Set SSL client Application Layer Protocol Negotiation (ALPN).
AT+CIPSSLCPSK: Query/Set SSL client Pre-shared Key (PSK).
AT+CIPRECONNINTV: Query/Set the TCP/UDP/SSL reconnection interval for the Wi-Fi normal transmission mode.
AT+CIPRECVMODE: Query/Set socket receiving mode.
AT+CIPRECVDATA: Obtain socket data in passive receiving mode.
AT+CIPRECVLEN: Obtain socket data length in passive receiving mode.
AT+PING: Ping the remote host.
AT+CIPDNS: Query/Set DNS server information.
AT+CIPTCPOPT: Query/Set the socket options.
AT+USERRAM: Operate user’s free RAM.
AT+USEROTA: Upgrade the firmware according to the specified URL.
AT+USERWKMCUCFG: Configure how AT wakes up MCU.
AT+USERMCUSLEEP: MCU indicates its sleep state.
AT+USERDOCS: Query the ESP-AT user guide for current firmware.
AT+DRVADC: Read ADC channel value.
AT+DRVPWMINIT: Initialize PWM driver.
AT+DRVPWMDUTY: Set PWM duty.
AT+DRVPWMFADE: Set PWM fade.
AT+DRVI2CINIT: Initialize I2C master driver.
AT+DRVI2CRD: Read I2C data.
AT+DRVI2CWRDATA: Write I2C data.
AT+DRVI2CWRBYTES: Write no more than 4 bytes I2C data.
AT+DRVSPICONFGPIO: Configure SPI GPIO.
AT+DRVSPIINIT: Initialize SPI master driver.
AT+DRVSPIRD: Read SPI data.
AT+DRVSPIWR: Write SPI data.AT+CIPV6: Enable/disable the network of Internet Protocol Version 6 (IPv6).
AT+CIPSTATUS: Obtain the TCP/UDP/SSL connection status and information.
AT+CIPV6: .
AT+CWMODE: Set the Wi-Fi mode (Station/SoftAP/Station+SoftAP).
AT+CWSTATE: Query the Wi-Fi state and Wi-Fi information.
AT+CWJAP: Connect to an AP.
AT+CWRECONNCFG: Query/Set the Wi-Fi reconnecting configuration.
AT+CWLAPOPT: Set the configuration for the command AT+CWLAP.
AT+CWLAP: List available APs.
AT+CWQAP: Disconnect from an AP.
AT+CWSAP: Query/Set the configuration of an ESP SoftAP.
AT+CWLIF: Obtain IP address of the station that connects to an ESP SoftAP.
AT+CWQIF: Disconnect stations from an ESP SoftAP.
AT+CWDHCP: Enable/disable DHCP.
AT+CWDHCPS: Query/Set the IP addresses allocated by an ESP SoftAP DHCP server.
AT+CWAUTOCONN: Connect to an AP automatically when powered on.
AT+CWAPPROTO: Query/Set the 802.11 b/g/n protocol standard of SoftAP mode.
AT+CWSTAPROTO: Query/Set the 802.11 b/g/n protocol standard of station mode.
AT+CIPSTAMAC: Query/Set the MAC address of an ESP station.
AT+CIPAPMAC: Query/Set the MAC address of an ESP SoftAP.
AT+CIPSTA: Query/Set the IP address of an ESP station.
AT+CIPAP: Query/Set the IP address of an ESP SoftAP.
AT+CWSTARTSMART: Start SmartConfig.
AT+CWSTOPSMART: Stop SmartConfig.
AT+WPS: Enable the WPS function.
AT+MDNS: Configure the mDNS function.
[ESP32 Only] AT+CWJEAP: Connect to a WPA2 Enterprise AP.
AT+CWHOSTNAME: Query/Set the host name of an ESP station.
AT+CWCOUNTRY: Query/Set the Wi-Fi Country Code.
AT+CWAPPROTO
ATE0
ATE1
AT+SYSREG"""

output = output.split("\"")

standard_commands = re.sub(r':[^.]+.', '',standard_commands)
standard_commands = standard_commands.split("\n")

hifive_cmds = []


for word in output:
    if "CMD" in word:
        word = word[::-len("CMD:57,")]
    if "AT" in word:
        hifive_cmds.append(word)


for word in hifive_cmds:
    if word not in standard_commands:
        print(word)