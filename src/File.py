class File:
    def __init__(self, filemd5, filename, ndownload):
        self.filemd5 = filemd5
        self.filename = filename
        self.ndownload = ndownload
        self.peers = []
    
    def insert(self, database, sessionid):
        
        #database.execute("""SELECT *
        #                    FROM file
        #                    WHERE filemd5 = %s""",
        #                    self.filemd5)
        database.execute("""SELECT filemd5, filename, ndownload
                            FROM file
                            WHERE filemd5 = %s""",
                            self.filemd5)
        
        find = True
        try:
            filemd5, filename, ndownload = dabase.fetchone()
        except:
            find = False
        
        if find:
            
            self.update(database, self.filename, ndownload) # filename potrebbe essere diverso, mentre ndownload è quello trovato dal database
            
        else:

            database.execute("""INSERT INTO file
                                (filemd5, filename, ndownload)
                                VALUES (%s, %s, %s)""",
                                (self.filemd5, self.filename, self.ndownload))

        try:
            database.execute("""INSERT INTO peer_has_file
                                (peer_sessionid, file_filemd5)
                                VALUES
                                (%s, %s)""",
                                (sessionid, self.filemd5))
        except:
            pass
    
    def update(self, database, filename, ndownload):
        self.filename = filename
        self.ndownload = ndownload
        
        database.execute("""UPDATE file
                            SET filename = %s, ndownload = %s
                            WHERE filemd5 = %s""",
                            (self.filename, self.ndownload, self.filemd5))
    
    def delete(self, database, sessionid):
        
        database.execute("""DELETE FROM peer_has_file
                            WHERE peer_sessionid = %s AND file_filemd5 = %s""",
                            (sessionid, self.filemd5))
        
        try:
            database.execute("""DELETE FROM file
                                WHERE filemd5 = %s""",
                                (self.filemd5))
        except:
            pass
    
    #def setPeers(self, peers):
    #    self.peers = peers
