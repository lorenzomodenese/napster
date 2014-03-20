class File:
    def __init__(self, filemd5, filename, ndownload):
        self.filemd5 = filemd5
        self.filename = filename
        self.ndownload = ndownload
        self.peers = []
    
    def insert(self, database, sessionid):
        
        #database.execute("""SELECT filemd5, filename, ndownload
        #                    FROM file
        #                    WHERE filemd5 = %s""",
        #                    self.filemd5)
        #
        #try:
        #    filemd5, filename, ndownload = database.fetchone()
        #    
        #    # se il file esiste gia', memorizzo ndownload nell'oggetto e aggiorno il file sul database 
        #    # filename potrebbe essere diverso, mentre ndownload rappresenta quello trovato dal database
        #    self.ndownload = ndownload
        #    self.update(database, self.filename, self.ndownload)
        #    
        #except:
        try:
            database.execute("""INSERT INTO file
                                (filemd5, filename, ndownload)
                                VALUES (%s, %s, %s)""",
                                (self.filemd5, self.filename, self.ndownload))
        except:
            pass

        try:
            database.execute("""INSERT INTO peer_has_file
                                (peer_sessionid, file_filemd5)
                                VALUES
                                (%s, %s)""",
                                (sessionid, self.filemd5))
        except:
            pass
    
    def update(self, database):
        
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
