# coding: utf-8
import socket
import os
import Peer
import PeerService
import File
import FileService
import Connessione

def adattaStringa(lunghezzaFinale, stringa):
    ritorno=stringa
    for i in range(len(stringa), lunghezzaFinale):
        ritorno="0"+ritorno
    return ritorno

def elimina_spazi_iniziali_finali(stringa):
    ritorno=""
    ritorno2=""
    lettera=False
    lettera2=False
    for i in range (0,len(stringa)):
        if(stringa[i]!=" " or lettera==True):
            ritorno=ritorno+stringa[i]
            lettera = True
   
    ritorno= ritorno[::-1]   

    for i in range (0,len(ritorno)):
        if(ritorno[i]!=" " or lettera2==True):
            ritorno2=ritorno2+ritorno[i]
            lettera2 = True

    return ritorno2[::-1]

    

host = "::1"#fd00::7cd7:4c32:8ff2:592b"
porta = 3000
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
            try:
                while 1:  #mi controllo la persistenza del peer
                    stringa_ricevuta = client.recv(size)
                    if stringa_ricevuta== "":
                        print("\t\tsocket vuota")
                        break
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
                        fileMD5=stringa_ricevuta[20:36]
                        fileName=stringa_ricevuta[36:136]
                        print ("\t\tOperazione AddFile SessionID: "+sessionID+" MD5: "+fileMD5+" Nome: "+fileName)

                        conn_db=Connessione.Connessione()
                        FileService.FileService.insertNewFile(conn_db.crea_cursore(), sessionID, fileMD5.upper(), fileName.upper())
                        count = FileService.FileService.getNCopy(conn_db.crea_cursore(), fileMD5.upper())
                        conn_db.esegui_commit()
                        conn_db.chiudi_connessione()

                        ncopie=adattaStringa(3, str(int(count) ) )
                        print("\t\tRestituisco: "+"AADD" + ncopie )
                        client.send("AADD" + ncopie )

            #operazione delete File         
                    if operazione.upper()=="DELF":
                        sessionID=stringa_ricevuta[4:20]
                        fileMD5=stringa_ricevuta[20:36]
                        print ("\t\tOperazione DeleteFile SessionID: "+sessionID+" MD5: "+fileMD5.upper())

                        conn_db=Connessione.Connessione()
                        file = FileService.FileService.getFile(conn_db.crea_cursore(), fileMD5.upper())
                        file.delete(conn_db.crea_cursore(), sessionID)
                        count = FileService.FileService.getNCopy(conn_db.crea_cursore(), fileMD5.upper())
                        conn_db.esegui_commit()
                        conn_db.chiudi_connessione()

                        ncopie=adattaStringa(3, str(int(count) ) )
                        print("\t\tRestituisco: "+"ADEL"+ ncopie)
                        client.send("ADEL"+ ncopie )

            #operazione Ricerca File         
                    if operazione.upper()=="FIND":
                        sessionID=stringa_ricevuta[4:20]
                        search=stringa_ricevuta[20:40]
                        #print("*"+search+"*")
                        search=elimina_spazi_iniziali_finali(search)
                        print ("\t\tOperazione Find SessionID: "+sessionID+" Parametro ricerca:  #"+search+"#")
                        
                        risultatoRicerca="AFIN"
                        conn_db=Connessione.Connessione()
                        files = FileService.FileService.getFiles(conn_db.crea_cursore(), search.upper())
                        i = 0
                        occorrenzeMD5=len(files)
                        risultatoRicerca=risultatoRicerca+adattaStringa(3, str(occorrenzeMD5))
                        print ("\t\tNumero file trovati (idmd5): " + str(occorrenzeMD5) )

                        while i < len(files):
                            print "\t\tfilemd5: ", files[i].filemd5
                            risultatoRicerca=risultatoRicerca+files[i].filemd5
                            
                            print "\t\tfilename: ", files[i].filename
                            risultatoRicerca=risultatoRicerca+files[i].filename
                            
                            print "ndownload: ", files[i].ndownload

                            print "\t\tNumero copie: ", len(files[i].peers)
                            risultatoRicerca=risultatoRicerca+adattaStringa(3, str(len(files[i].peers)))

                            j = 0
                            while j < len(files[i].peers):
                                #print "sessionid: ", files[i].peers[j].sessionid
                                print "\t\t\tipp2p: ", files[i].peers[j].ipp2p
                                risultatoRicerca=risultatoRicerca+files[i].peers[j].ipp2p
                                
                                print "\t\t\tpp2p: ", files[i].peers[j].pp2p
                                risultatoRicerca=risultatoRicerca+files[i].peers[j].pp2p
                                
                                j = j + 1
                            print ""
                            i = i + 1
                            
                            
                        conn_db.esegui_commit()
                        conn_db.chiudi_connessione()


                        print("\t\tRestituisco: "+ risultatoRicerca)
                        client.send(risultatoRicerca )

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
                        fileMD5=stringa_ricevuta[20:36]
                        print ("\t\tOperazione NotificaDownload SessionID: "+sessionID+" MD5: "+fileMD5.upper())

                        conn_db=Connessione.Connessione()
                        file = FileService.FileService.getFile(conn_db.crea_cursore(), fileMD5.upper())
                        file.update(conn_db.crea_cursore(), (file.filename).upper(), int(file.ndownload) + 1)
                        conn_db.esegui_commit()
                        conn_db.chiudi_connessione()

                        ncopie=adattaStringa(5, str(int(file.ndownload) ) )  
                        print("\t\tRestituisco: "+"ADRE" + ncopie )
                        client.send("ADRE" + ncopie )
            
            except Exception as nonpersistente:
                print e
                print("Connessione non persistente")
                
        except Exception as e: 
            print e
            print("Errore ricezione")
        finally:
            client.close() 
            os._exit(0) 
    else:
        client.close()
    
print("Terminato server")