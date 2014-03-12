import string
import random

class Peer:
    def __init__(self, sessionid, ipp2p, pp2p):
        self.sessionid = sessionid
        self.ipp2p = ipp2p
        self.pp2p = pp2p
    
    def insert(self, database):
        
        #generazione sessionid
        self.sessionid = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        
        #check di unicita'
        database.execute("""SELECT sessionid
                            FROM peer
                            WHERE sessionid = %s""",
                            (self.sessionid))
        while database.fetchone() != None:
            self.sessionid = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            database.execute("""SELECT sessionid
                                FROM peer
                                WHERE sessionid = %s""",
                                (self.sessionid))
        
        #inserimento nuovo peer
        database.execute("""INSERT INTO peer
                            (sessionid, ipp2p, pp2p)
                            VALUES
                            (%s, %s, %s)""",
                            (self.sessionid, self.ipp2p, self.pp2p))
        
    #def update(self, database): 
        #pass
    
    def delete(self, database):
        
        database.execute("""DELETEF FROM peer_has_file
                            WHERE peer_sessionid = %s""",
                            self.sessionid)
        
        database.execute("""DELETE FROM file
                            WHERE filemd5 NOT IN (SELECT file_filemd5
                                                  FROM peer_has_file)""")
        
        database.execute("""DELETE FROM peer
                            WHERE sessionid = %s""",
                            self.sessionid)
