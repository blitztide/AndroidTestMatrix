import MySQLdb as my
import AndroidTrustMatrix.Marketplaces as MP
import AndroidTrustMatrix.Domains as DM

class db():
    """db class abstracts all db functionality"""

    def Connect(self,username, password, host, port, database):
        self.db = my.connect(host,username,password,database)
        print(f'Connected: {username}@{host}:{port}/{database}')

    def Get_Markets(self):
        """Extracts all known Marketplaces from DB and returns Marketplace objects"""
        cursor = self.db.cursor(my.cursors.DictCursor)
        cursor.execute("SELECT Marketplace.MarketID,Marketplace.name,Domains.URI FROM Marketplace INNER JOIN Domains ON Domains.DomainID=Marketplace.Domain")
        markets = []
        for row in cursor.fetchall():
            markets.append(MP.Marketplace(row["MarketID"],row["name"],row["URI"]))
        cursor.close()
        return markets

    def Disconnect(self):
        if(self.db):
            self.db.close()
    
    def __del__(self):
        if (self.db):
            self.db.close()
