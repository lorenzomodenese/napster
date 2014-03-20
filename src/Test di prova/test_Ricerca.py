import MySQLdb
import FileService

db = MySQLdb.connect(user="napster", passwd="napster", db="napster")
c = db.cursor()

files = FileService.FileService.getFiles(c, "stA")

i = 0
occorrenzeMD5=len(files)

print ("Numero file trovati (idmd5): ", occorrenzeMD5)

while i < len(files):
    print "filemd5: ", files[i].filemd5
    print "filename: ", files[i].filename
    #print "ndownload: ", files[i].ndownload
    
    print "Numero copie: ", len(files[i].peers)
    
    j = 0
    while j < len(files[i].peers):
        print "sessionid: ", files[i].peers[j].sessionid
        print "ipp2p: ", files[i].peers[j].ipp2p
        print "pp2p: ", files[i].peers[j].pp2p
        j = j + 1
    
    print ""
    i = i + 1

db.commit()