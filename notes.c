//uncomment for all command printout
  //   for (int i = 0 ; i < 75 ; i ++ ){
  //     for (int j = 0 ; j < buf_len ; j ++){
  //       buf[j] = 0;
  //     }

  //     esp_comm("AT+CMD?\r\n", (char *) 0x8001150,i,0,75);
      
  //     for (int k = 0 ; k < buf_len ; k ++){
  //       priv_printf("%c", buf[k]);
  //     }
  // }
  
  
  
  
  // esp_comm("AT+DBG_TOKEN?\r\n",(char*) 0x8001150,0,0,4);
  // for (int k = 0 ; k < buf_len ; k ++){
  //       priv_printf("%c", buf[k]);
  //     }

  // int debug_token = *buf;

  //esp_comm("AT+SECLAB?\r\n",(char*) 0x8001150,0,0,50);
  OUTPUT: SecLab feature present! Initialize with exec 
                                                 ----
  command, check heartbeat with set command (expects length and a string to be echoed)

  //AT+DBGTOKEN?  

