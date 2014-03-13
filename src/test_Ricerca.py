import MySQLdb
import FileService

db = MySQLdb.connect(user="napster", passwd="napster", db="napster")
c = db.cursor()

files = FileService.FileService.getFiles(c, "stA")

i = 0
#print len(files)
while i < len(files):
    print files[i].filemd5
    print files[i].filename
    print files[i].ndownload
    
    j = 0
    while j < len(files[i].peers):
        print files[i].peers[j].sessionid
        print files[i].peers[j].ipp2p
        print files[i].peers[j].pp2p
        j = j + 1
    
    i = i + 1

db.commit()