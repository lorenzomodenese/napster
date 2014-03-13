import File
import sys

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
    
    @staticmethod
    def getFiles(database, searchString):
        searchString = "%" + searchString + "%"
        database.execute("""SELECT filename, filemd5, ndownload, sessionid, ipp2p, pp2p
                            FROM file, peer, peer_has_file
                            WHERE file_filemd5 = filemd5 AND
                                  peer_sessionid = sessionid AND
                                  filename LIKE %s
                            ORDER BY filemd5, sessionid""",
                            searchString)
        
        #print database._last_executed
        
        try:
            i = 0
            files = []
            peers = []
            previous_filemd5 = ""
            while True:
            
                filename, filemd5, ndownload, sessionid, ipp2p, pp2p = database.fetchone()
                print filename, filemd5, ndownload, sessionid, ipp2p, pp2p
                
                if filemd5 != previous_filemd5:
                    files.append(File.File(filemd5, filename, ndownload))
                    #print files[i].filemd5
                    j = 0
                    peers = []
                    files[i].setPeers(peers)
                    previous_filemd5 = filemd5
                    i = i + 1
                
                print "ciao"
                print len(files[i].peers), "Ciao"
                files[i].peers.append(Peer.Peer(sessionid, ipp2p, pp2p))
                print len(files[i].peers)
                print "ciao"
                print files[i].peers[j].sessionid
                j = j + 1
        
        except:
            print sys.exc_info()
            
        return files
        
        