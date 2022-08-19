import datetime
import MySQLdb as my
from MySQLdb.cursors import DictCursor
import AndroidTrustMatrix.Marketplaces as MP
import AndroidTrustMatrix.Domains as DM

class db():
    """db class abstracts all db functionality"""

    def Connect(self,username, password, host, port, database):
        """Initialise connection to database"""
        self.db = my.connect(host,username,password,database)
        print(f'Connected: {username}@{host}:{port}/{database}')

    def Get_Markets(self):
        """Extracts all known Marketplaces from DB and returns Marketplace objects"""
        cursor = self.db.cursor(my.cursors.DictCursor)
        cursor.execute("SELECT Marketplace.MarketID,Marketplace.name,Domains.URI,Marketplace.Company FROM Marketplace INNER JOIN Domains ON Domains.DomainID=Marketplace.Domain")
        markets = []
        for row in cursor.fetchall():
            MarketID = row["MarketID"]
            name = row["name"]
            URI = row["URI"]
            if "Company" in row.keys():
                Company = row["Company"]
            else:
                Company = 0

            markets.append(MP.Marketplace(MarketID,name,URI,Company))
        cursor.close()
        return markets
    
    def Get_CompanyInfo(self,market):
        """Extracts all relevant Company Information for a given Market to return as a dict"""
        company = {}
        company["Exists"] = False
        CompanyID = market.Company
        if not CompanyID == None:
            cursor = self.db.cursor(my.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM Companies WHERE CompanyID = {CompanyID}")
            for row in cursor.fetchall():
                company["Exists"] = row["Exists"]
                company["Founded"] = row["Founded"]
            cursor.close()
            dateformat = "%Y-%m-%d %H:%M:%S"
            StartDate = datetime.strptime(company["Founded"],dateformat)
            Today = datetime.today().strftime(dateformat)
            diff = Today - StartDate
            company["Age"] = diff.days
        return company
    
    def Get_Incidents(self,company):
        """Returns a list of incidents for a given company"""
        incidents = []
        cursor = self.db.cursor(my.cursors.DictCursor)
        cursor.execute(f"SELECT IncidentDate FROM Incidents WHERE Company = {company}")
        incidents = cursor.fetchall()
        return incidents
    
    def Update_CompanyScore(self,market,Tcompany):
        """Update database with new CompanyScore"""
        print(f"New Company Score {Tcompany} for {market}")
        cursor = self.db.cursor()
        query = f"UPDATE Marketplace SET CompanyScore = {int(Tcompany)} WHERE MarketID={market.id}"
        cursor.execute(query)
        cursor.close()
        return

    def Update_DomainScore(self,market,Tdomain):
        """Update database with new DomainScore"""
        print(f"New Domain Score {Tdomain} for {market}")
        cursor = self.db.cursor()
        query = f"UPDATE Marketplace SET DomainScore = {int(Tdomain)} WHERE MarketID={market.id}"
        cursor.execute(query)
        cursor.close()
        return
    
    def Update_MarketScore(self,market,Tmarket):
        """Update database with new MarketScore"""
        print(f"New Market Score {Tmarket} for {market}")
        cursor = self.db.cursor()
        query = f"UPDATE Marketplace SET CompanyScore = {int(Tmarket)} WHERE MarketID={market.id}"
        cursor.execute(query)
        cursor.close()
        return

    def Add_Certificate(self,domain,certificate,fingerprint):
        """Add a found certificate to the database"""
        return

    def Add_Application(self,pkg_name,version,isMalware,md5sum,sha1sum,sha256sum,appDate,AddedDate):
        """Add a found application to the database"""
        return

    def Disconnect(self):
        """Close connection to database"""
        if(self.db):
            self.db.close()
    
    def __del__(self):
        if (self.db):
            self.db.commit()
            self.db.close()
