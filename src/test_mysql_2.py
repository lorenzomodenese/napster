import MySQLdb
import PeerService
import Peer

db = MySQLdb.connect(user="napster", passwd="napster", db="napster")
c = db.cursor()

peer = PeerService.PeerService.insertNewPeer(c, "0000:0000:0000:0000:0000:0000:0000:0011", "8081")
print peer.sessionid

db.commit()