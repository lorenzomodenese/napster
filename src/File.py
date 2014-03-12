class File:
    def __init__(self, filemd5, filename, ndownload):
        self.filemd5 = filemd5
        self.filename = filename
        self.ndownload = ndownload
    
    def insert(self, database, sessionid):
        try:
            database.execute("""INSERT INTO file
                                (filemd5, filename, ndownload)
                                VALUES
                                (%s, %s, %s)""",
                                (self.filemd5, self.filename, self.ndownload))
        except:
            pass
        finally:
             database.execute("""INSERT INTO peer_has_file
                                 (peer_sessionid, file_filemd5)
                                 VALUES
                                 (%s, %s)""",
                                 (sessionid, self.filemd5))
    
    def update(self, database, filename, ndownload):
        database.execute("""UPDATE file
                            SET filename = %s, ndownload = %s
                            WHERE filemd5 = %s""",
                            (filename, ndownload, self.filemd5))
    
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