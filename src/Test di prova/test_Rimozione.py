import MySQLdb
import PeerService
import Peer
import FileService
import File

sessionid = "8EMIIRBQYMF213W3"
#sessionid = "0000000000000001"
filemd5 = "1234567890123456"

db = MySQLdb.connect(user="napster", passwd="napster", db="napster")
c = db.cursor()

file = FileService.FileService.getFile(c, filemd5)
file.delete(c, sessionid)

count = FileService.FileService.getNCopy(c, filemd5)
print count

db.commit()