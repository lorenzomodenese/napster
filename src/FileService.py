import File

class FileService:
    
    @staticmethod
    def insertNewFile(database, sessionid, filemd5, filename):
        file = File.File(filemd5, filename, 0)
        file.insert(database, sessionid)
        return file
    
    @staticmethod
    def getFile(database, filemd5):
        database.execute("""SELECT filemd5, filename, ndownload
                            FROM file
                            WHERE filemd5 = %s""",
                            filemd5)
        filemd5, filename, ndownload = database.fetchone()
        file = File.File(filemd5, filename, ndownload)
        return file
    
    @staticmethod
    def getNCopy(database, filemd5):
        database.execute("""SELECT count(*)
                            FROM peer_has_file
                            WHERE file_filemd5 = %s""",
                            filemd5)
        count, = database.fetchone()
        return count
    