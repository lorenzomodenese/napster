import MySQLdb
import Peer
import PeerService
import File

db = MySQLdb.connect(user="napster", passwd="napster", db="napster")

c = db.cursor()
c.execute("""SELECT * FROM peer""")
try:
    aa, bb, cc = c.fetchone()
    aa, bb, cc = c.fetchone()
    print c.fetchone()
    print aa, bb, cc
except:
    print "Errore"

peer = Peer.Peer("0000:0000:0000:0000:0000:0000:0000:0011", "9999", "1")
#peer = Peer.Peer("0000:0000:0000:0000:0000:0000:0000:0011", "9999")
peer2 = Peer.Peer("0000:0000:0000:0000:0000:0000:0000:0010", "9999", "1")

peer.insert(c)

db.commit()

peer2.insert(c)
db.commit()

#peer.delete(c)
#db.commit()

file = File.File("01", "Test", 5)

file.insert(c, peer.sessionid)
db.commit()
file.insert(c, peer2.sessionid)
db.commit()

file.update(c, "TestProva", 6)

file.delete(c, peer.sessionid)

db.commit()