# coding: utf-8
#from pymysql.connections import length
import socket
import os

host = "::1"#'fd00::69df:154b:38fd:beb6'
porta = 3000
size=1024

print("avvio directory")
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,porta))
s.listen(5)
while 1:
    print("attesa connessione peer")
    client, address = s.accept()
    newpid = os.fork()
    if(newpid==0):
        try:
            s.close()
            stringa_ricevuta = client.recv(size)
            print("\tMESSAGGIO RICEVUTO: "+stringa_ricevuta.decode())
            operazione=stringa_ricevuta[0:4]
            
            
            if operazione.upper()=="LOGI":
                ipp2p=stringa_ricevuta[4:43]
                pp2p=stringa_ricevuta[43:48]
                print ("\t\tOperazione Login ipp2p: "+ipp2p+" porta: "+pp2p)
                #Peer peer= Peer.Peer(ipp2p,pp2p) #no session id
                
                sessionID="0123456789abcdef"
                client.send("ALGI"+sessionID)
              
            if operazione.upper()=="ADDF":
                sessionID=stringa_ricevuta[4:20]
                fileMD5=stringa_ricevuta[20:35]
                fileName=stringa_ricevuta[35:100]
                print ("\t\tOperazione AddFile SessionID: "+sessionID+" MD5: "+fileMD5+" Nome: "+fileName)
                #operazioni aggiunta
                
                ncopie="999"
                client.send("AADD"+ncopie)
        except Exception as e: 
            print e
            print("Errore ricezione")
        finally:
            client.close() 
            os._exit(0) 
    else:
        client.close()
    
print("terminato server")
    

