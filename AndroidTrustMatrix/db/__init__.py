import MySQLdb as my

class db():
    def __init__(self):
        return
    def Connect(self,username, password, host, port, database):
        self.db = my.connect(host,username,password,database)
        print(f'Connected: {username}@{host}:{port}/{database}')

    def Get_Markets(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT MarketID,name FROM Marketplace")
        markets = {}
        for row in cursor.fetchall():
            markets[row[1]]=row[0]
        cursor.close()
        return markets

    def Disconnect():
        return True
