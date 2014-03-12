import MySQLdb

class Connessione:
    def __init__(self):
        try:
           
            self.db = MySQLdb.connect(host="localhost", # your host, usually localhost
                                  user="root", # your username
                                  passwd="lucaluca", # your password
                                  db="napster") # name of the data base
        
        except Exception as e: 
            print e
            print("Errore crea db")
        
                           
                             
    def crea_cursore(self):
        try:
            cur = self.db.cursor()
        except Exception as e: 
            print e
            print("Errore crea cursore")
        return cur
        
        
    def esegui_commit(self):
        try:
            self.db.commit()
        except Exception as e: 
            print e
            print("Errore esegui commit")
            
            
    def chiudi_connessione(self):
        try:
            self.db.close()
        except Exception as e: 
            print e
            print("Errore chiudi connessione")
        