# coding: utf-8
#   PEER DI PROVA !!!
import socket
import sys

HOST, PORTA = '::1', 3000
stringa_da_trasmettere="LOGIfd00:0000:0000:0000:69df:154b:38fd:beb799999"
stringa_da_trasmettere="LOGOLZC7RCTC1AFYYU6I"
stringa_da_trasmettere3="ADDFLZC7RCTC1AFYYU6I12345678901234X1"#per aggiunta file
stringa_da_trasmettere3="DELFD3HIK5038VUK57GE12345678901234X3"#per eliminazione file

#GK6W2XSOP4BQA568    5BCF5E7K30Q6A0JG
#stringa_da_trasmettere="DREGHW0CU2X3CGYR4XBV12345678901234X2"#per aggiunta file
stringa_da_trasmettere3="FINDLZC7RCTC1AFYYU6I.  ciao a tutti .  "

print("client apre socket")
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock.connect((HOST, PORTA))

try:
    #for n in range(0, 100):
       # if ((n % 10)==0):
       #     stringa_da_trasmettere=stringa_da_trasmettere+"-"
      #  else:
     #       stringa_da_trasmettere=stringa_da_trasmettere+"A"
    #for n in range(0, 100):
    #    stringa_da_trasmettere=stringa_da_trasmettere+""
    
    print("-->invio messaggio: "+stringa_da_trasmettere)
    sock.send(stringa_da_trasmettere.encode())
    ricevuto=sock.recv(2040);
    
    print("ho ricevuto "+ricevuto)
    
    #per verificare la persistenza
    
    #x = raw_input("--------Enter a number:")
   # 
   # stringa2="LOGO"+x
   # print("voglio inviare "+stringa2)
   # sock.send(stringa2.encode())
   # ricevuto=sock.recv(1024);
    #print(ricevuto)
    
    
    
except:
    print("Errore")


sock.close()
print("Termino client")
