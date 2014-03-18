#!/usr/bin/python 
#peer di esempio per interfacciarsi alla directory

import socket               

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)         
#host = 'fd00:0000:0000:0000:4059:03a1:3410:8012' Lorenzo
#host = 'fd00:0000:0000:0000:18f4:832b:b563:b1c5' Luca
#host = 'fd00:0000:0000:0000:a617:31ff:fe0f:822e' Paolo
host = 'fd00:0000:0000:0000:22c9:d0ff:fe47:70a3'

port = 3000                

s.connect((host, port))
print "Connesso!"

sessionid = ""
loggedin = False

while 1:
    print "\n\t\t\t----Test----"
    print "\t1. Login\n\t2. Add File\n\t3. Remove File\n\t4. Find file\n\t5. Download File\n\t6. Logout\n\t7. Chiudi modulo test"
    user = raw_input("Choose test:")
    if user == "1":
        ip = raw_input("IP address:")
        port = raw_input("Port:")    
        if len(ip) == 39 and len(port) == 5:
            s.send("LOGI"+ip+port)        
            response = s.recv(1024)
            if response[0:4] == "ALGI":
                print "\t--> Ok"
                sessionid = response[4:20]
                loggedin = True
                print "Session ID:"+sessionid
            else: 
                print response
        else: 
            print "Paramaters not correct"
            
    if user == "2":
        if loggedin == True:
            MD5 = raw_input("File MD5:")
            name = raw_input("File name:")
            if len(MD5) == 16 and len(name) <= 100:
                s.send("ADDF"+sessionid+MD5+name)
                response = s.recv(1024)
                if response[0:4] == "AADD":
                    print "\t--> Ok"            
                    print "Number of copies:"+response[4:7] 
                else: 
                    print response      
            else: 
                print "Parameters not correct"
        else:
            print "Please, login first!"
    
    if user == "3":
        if loggedin == True:
            MD5 = raw_input("File MD5:")        
            if len(MD5) == 16:
                s.send("DELF"+sessionid+MD5)
                response = s.recv(1024)
                if response[0:4] == "ADEL":
                    print "\t--> Ok"            
                    print "Number of copies:"+response[4:7]
                else: 
                    print response       
            else: 
                print "Parameters not correct"
        else:
            print "Please, login first!"
            
    if user == "4":
        if loggedin == True:
            searchString = raw_input("Search string:")        
            if len(searchString) <= 20:
                s.send("FIND"+sessionid+searchString)
                response = s.recv(1024)
                if response[0:4] == "AFIN":
                    print "\t--> Ok"
                    print response 
                else: 
                    print response                  
            else: 
                print "Parameters not correct"
        else:
            print "Please, login first!"
            
    if user == "5":
        if loggedin == True:
            MD5 = raw_input("File MD5:")        
            if len(MD5) == 16:
                s.send("DREG"+sessionid+MD5)
                response = s.recv(1024)
                if response[0:4] == "ADRE":
                    print "\t--> Ok"
                    print "Number of downloads:"+response[4:9]
                else: 
                    print response                   
            else: 
                print "Parameters not correct"
        else:
            print "Please, login first!"
            
    if user == "6":
        if loggedin == True:        
            s.send("LOGO"+sessionid)
            response = s.recv(1024)
            if response[0:4] == "ALOG":
                print "\t--> Ok"
                print "Number of files deleted:"+response[4:7] 
            else: 
                print response              
        else:
            print "Please, login first!"
    
    if user == "7":    
        s.close  
        print "Closed."
        break                   
