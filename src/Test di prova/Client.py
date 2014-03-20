#!/usr/bin/python
import socket

class TestPeer:    
    
    @staticmethod
    def connect(host, port):
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        try:        
            s.connect((host, port))
            print "\t--->Succesfully connected!\n"
            return s
        except:
            print "--!!!--> Connection error! <--!!!--\nTerminated."
            exit(1)
            
    @staticmethod
    def disconnect(s):
        s.close()

    @staticmethod
    def peer(sockHost, sockPort):     
        print "\n\t\t--------Starting test module----------\n"     
        
        sessionid = ""
        loggedin = False
        connected = False
        
        persistent = False
        print "Available connection modes:\n\t1.Non-persistent\n\t2.Persistent"
        persistenceSelect = raw_input("\nSelect connection mode:")
        if persistenceSelect == "1":
            print "\t--->Non-persistent peer"
            persistent = False
        else:
            print "\t--->Persistent peer"
            persistent = True
        
        while 1:            
            print "\n\t\t\t----Test----"
            print "\t1. Login\n\t2. Add File\n\t3. Remove File\n\t4. Find file\n\t5. Download File\n\t6. Logout\n\t7. Chiudi modulo test"
            user = raw_input("\nChoose test:")
            if user == "1":
                if (not connected):
                    s = TestPeer.connect(sockHost, sockPort)
                    connected = True
                ip = raw_input("IP address:")
                port = raw_input("Port:")    
                if len(ip) == 39 and len(port) == 5:
                    s.send("LOGI"+ip+port)        
                    response = s.recv(1024)
                    if response[0:4] == "ALGI":
                        print "\t--> Ok"
                        sessionid = response[4:20]
                        if sessionid == "0000000000000000":
                            print "\tAnother client is logged in with the same parameters.\n\tPlease, change your choice."
                        else:
                            loggedin = True
                        print "\tSession ID:"+sessionid
                    else:
                        print "\t--!!!--> Unexpected response <--!!!--\n" 
                        print response
                else: 
                    print "--!!!--> Parameters not correct <--!!!--"
                if (not persistent):
                    TestPeer.disconnect(s)
                    connected = False           
                    
            if user == "2":
                if (not connected):
                    s = TestPeer.connect(sockHost, sockPort)
                    connected = True
                if loggedin == True:
                    MD5 = raw_input("File MD5:")
                    name = raw_input("File name:")
                    if len(MD5) == 16 and len(name) <= 100:
                        s.send("ADDF"+sessionid+MD5+name)
                        response = s.recv(1024)
                        if response[0:4] == "AADD":
                            print "\t--> Ok"            
                            print "\tNumber of copies:"+response[4:7] 
                        else:
                            print "\t--!!!--> Unexpected response <--!!!--\n" 
                            print response      
                    else: 
                        print "--!!!--> Parameters not correct <--!!!--"
                else:
                    print "\tPlease, login first!"
                if (not persistent):
                    TestPeer.disconnect(s)
                    connected = False
            
            if user == "3":
                if (not connected):
                    s = TestPeer.connect(sockHost, sockPort)
                    connected = True
                if loggedin == True:
                    MD5 = raw_input("File MD5:")        
                    if len(MD5) == 16:
                        s.send("DELF"+sessionid+MD5)
                        response = s.recv(1024)
                        if response[0:4] == "ADEL":
                            print "\t--> Ok"            
                            print "\tNumber of copies:"+response[4:7]
                        else:
                            print "\t--!!!--> Unexpected response <--!!!--\n" 
                            print response       
                    else: 
                        print "--!!!--> Parameters not correct <--!!!--"
                else:
                    print "\tPlease, login first!"
                if (not persistent):
                    TestPeer.disconnect(s)
                    connected = False
                    
            if user == "4":
                if (not connected):
                    s = TestPeer.connect(sockHost, sockPort)
                    connected = True
                if loggedin == True:
                    searchString = raw_input("Search string:")        
                    if len(searchString) <= 20:
                        s.send("FIND"+sessionid+searchString)
                        response = s.recv(1024)
                        if response[0:4] == "AFIN":
                            print "\t--> Ok"
                            print response 
                        else:
                            print "\t--!!!--> Unexpected response <--!!!--\n" 
                            print response                  
                    else: 
                        print "--!!!--> Parameters not correct <--!!!--"
                else:
                    print "\tPlease, login first!"
                if (not persistent):
                    TestPeer.disconnect(s)
                    connected = False
                    
            if user == "5":
                if (not connected):
                    s = TestPeer.connect(sockHost, sockPort)
                    connected = True
                if loggedin == True:
                    MD5 = raw_input("File MD5:")        
                    if len(MD5) == 16:
                        s.send("DREG"+sessionid+MD5)
                        response = s.recv(1024)
                        if response[0:4] == "ADRE":
                            print "\t--> Ok"
                            print "\tNumber of downloads:"+response[4:9]
                        else:
                            print "\t--!!!--> Unexpected response <--!!!--\n" 
                            print response                   
                    else: 
                        print "--!!!--> Parameters not correct <--!!!--"
                else:
                    print "\tPlease, login first!"
                if (not persistent):
                    TestPeer.disconnect(s)
                    connected = False
                    
            if user == "6":
                if (not connected):
                    s = TestPeer.connect(sockHost, sockPort)
                    connected = True
                if loggedin == True:        
                    s.send("LOGO"+sessionid)
                    response = s.recv(1024)
                    if response[0:4] == "ALGO":
                        print "\t--> Ok"
                        print "\tNumber of files deleted:"+response[4:7] 
                    else:
                        print "\t--!!!--> Unexpected response <--!!!--\n" 
                        print response              
                else:
                    print "\tPlease, login first!"
                if (not persistent):
                    TestPeer.disconnect(s)
                    connected = False
            
            if user == "7": 
                if (connected):   
                    TestPeer.disconnect(s)  
                print "\tClosed."
                break
def main():
    host = 'fd00:0000:0000:0000:5907:c299:3fd3:e5ea' #Lorenzo
    #host = 'fd00:0000:0000:0000:18f4:832b:b563:b1c5' #Luca
    #host = 'fd00:0000:0000:0000:a617:31ff:fe0f:822e' #Paolo
    #host = 'fd00:0000:0000:0000:24f4:0969:d4f2:ad07' #Davide
    #host = "::1"   
    #host = "::1"
    port = 3000
    
    TestPeer.peer(host, port)

if __name__=="__main__":
    main()                   
