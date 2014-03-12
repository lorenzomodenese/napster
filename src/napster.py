# coding: utf-8
import socket
import os
import Peer
import PeerService
import Connessione

def adattaStringa(lunghezzaFinale, stringa):
    ritorno=stringa
    for i in range(len(stringa), lunghezzaFinale):
        ritorno="0"+ritorno
    return ritorno
    

host = "::1"#'fd00::69df:154b:38fd:beb6'
porta = 5000
size=1024

print("Avvio directory")
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,porta))
s.listen(5)
while 1:
    print("Attesa connessione peer")
    client, address = s.accept()
    newpid = os.fork()
    if(newpid==0):
        try:
            s.close()
            stringa_ricevuta = client.recv(size)
            print("\tMESSAGGIO RICEVUTO: "+stringa_ricevuta.decode())
            operazione=stringa_ricevuta[0:4]
            
    #operazione Login
            if operazione.upper()=="LOGI":
                ipp2p=stringa_ricevuta[4:43]
                pp2p=stringa_ricevuta[43:48]
                print ("\t\tOperazione Login ipp2p: "+ipp2p+" porta: "+pp2p)
                
                conn_db=Connessione.Connessione()
                peer= PeerService.PeerService.insertNewPeer(conn_db.crea_cursore(), ipp2p, pp2p)
                conn_db.esegui_commit()
                conn_db.chiudi_connessione()
                sessionID=peer.sessionid
                
                print("\t\tRestituisco: "+"ALGI"+sessionID)
                client.send("ALGI"+sessionID)
                
    #operazione add File         
            if operazione.upper()=="ADDF":
                sessionID=stringa_ricevuta[4:20]
                fileMD5=stringa_ricevuta[20:35]
                fileName=stringa_ricevuta[35:135]
                print ("\t\tOperazione AddFile SessionID: "+sessionID+" MD5: "+fileMD5+" Nome: "+fileName)
                #operazioni aggiunta
                
                ncopie=adattaStringa(3, str(int("000000009") ) )
                print("\t\tRestituisco: "+"AADD" + ncopie )
                client.send("AADD" + ncopie )
                
    #operazione delete File         
            if operazione.upper()=="DELF":
                sessionID=stringa_ricevuta[4:20]
                fileMD5=stringa_ricevuta[20:35]
                print ("\t\tOperazione DeleteFile SessionID: "+sessionID+" MD5: "+fileMD5)
                #operazioni rimozione
                
                ncopie==adattaStringa(3, str(int("000000009") ) )
                print("\t\tRestituisco: "+"ADEL"+ ncopie)
                client.send("ADEL"+ ncopie )
                
    #operazione Ricerca File         
            if operazione.upper()=="FIND":
                sessionID=stringa_ricevuta[4:20]
                search=stringa_ricevuta[20:40]
                print ("\t\tOperazione Find SessionID: "+sessionID+" Parametro ricerca: "+search)
                #operazioni trova
                
                occorrenzeTrovate=adattaStringa(3, str(int("000000009") ) )
                result="elenco file da db"
                print("\t\tRestituisco: "+"AFIN"+ occorrenzeTrovate + result)
                client.send("AFIN" + occorrenzeTrovate + result )
                
        #operazione Logout         
            if operazione.upper()=="LOGO":
                sessionID=stringa_ricevuta[4:20]
                print ("\t\tOperazione LogOut SessionID: "+sessionID)
                
                conn_db=Connessione.Connessione()
                peer = PeerService.PeerService.getPeer(conn_db.crea_cursore(), sessionID)
                count = PeerService.PeerService.getCountFile(conn_db.crea_cursore(), sessionID)
                peer.delete(conn_db.crea_cursore())
                conn_db.esegui_commit()
                conn_db.chiudi_connessione()
                
                
                ncopieCancellate=adattaStringa(3, str(int(count) ) )
                print("\t\tRestituisco: "+"ALOG" + ncopieCancellate )
                client.send("ALOG" + ncopieCancellate )
                
        #operazione notifica Download File         
            if operazione.upper()=="DREG":
                sessionID=stringa_ricevuta[4:20]
                fileMD5=stringa_ricevuta[20:35]
                print ("\t\tOperazione NotificaDownload SessionID: "+sessionID+" MD5: "+fileMD5)
                #operazioni conteggio download
                
                ncopie=adattaStringa(5, str(int("000000009") ) )  
                print("\t\tRestituisco: "+"ADRE" + ncopie )
                client.send("ADRE" + ncopie )
                
        except Exception as e: 
            print e
            print("Errore ricezione")
        finally:
            client.close() 
            os._exit(0) 
    else:
        client.close()
    
print("Terminato server")
    

