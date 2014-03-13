import MySQLdb
import PeerService
import Peer
import FileService
import File

sessionid = "8EMIIRBQYMF213W3"
#sessionid = "0000000000000001"
filemd5 = "1234567890123456"
#filemd5 = "123456789012345!"

db = MySQLdb.connect(user="napster", passwd="napster", db="napster")
c = db.cursor()

file = FileService.FileService.insertNewFile(c, sessionid, filemd5, "TestAggiunta?")

count = FileService.FileService.getNCopy(c, file.filemd5)
print count

db.commit()