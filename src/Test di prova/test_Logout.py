import MySQLdb
import PeerService
import Peer
import FileService
import File

#sessionid = "8EMIIRBQYMF213W3"
sessionid = "0000000000000001"
filemd5 = "1234567890123456"

db = MySQLdb.connect(user="napster", passwd="napster", db="napster")
c = db.cursor()

peer = PeerService.PeerService.getPeer(c, sessionid)

count = PeerService.PeerService.getCountFile(c, sessionid)

# Prima si calcola il numero di file e poi si cancella il peer!
peer.delete(c)

print count

db.commit()