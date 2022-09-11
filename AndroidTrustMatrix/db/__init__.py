import datetime
import MySQLdb as my
import AndroidTrustMatrix.Marketplaces as MP
import AndroidTrustMatrix.config as Config

class db():
    """db class abstracts all db functionality"""

    def __init__(self):
        self.db = None
        self.username,self.password,self.host,self.port,self.database = Config.get_db_config()
        

    def Connect(self):
        """Initialise connection to database returns a db connection"""
        self.db = my.connect(self.host,self.username,self.password,self.database)
        #print(f'Connected: {self.username}@{self.host}:{self.port}/{self.database}')

    def Disconnect(self):
        """Close the connection to the database"""
        #print("Closing database connection")
        self.db.close()
        self.db = None

    def Analysed_Recently(self,market,app):
        """Checks if app has been seen in last 7 days"""
        query = ""
        return False

    def Get_Markets(self):
        """Extracts all known Marketplaces from DB and returns Marketplace objects"""
        query = "SELECT Marketplace.MarketID,Marketplace.name,Domains.URI,Marketplace.Company FROM Marketplace INNER JOIN Domains ON Domains.DomainID=Marketplace.Domain"
        markets = []
        rows = self._dict_query(query)
        for row in rows:
            MarketID = row["MarketID"]
            name = row["name"]
            uri = row["URI"]
            if "Company" in row.keys():
                Company = row["Company"]
            else:
                Company = None

            markets.append(MP.Marketplace(MarketID,name,uri,Company))
        return markets
    
    def Get_CompanyInfo(self,market):
        """Extracts all relevant Company Information for a given Market to return as a dict"""
        company = {}
        company["Exists"] = False
        CompanyID = market.Company
        # CompanyID = 1 means it isn't a company
        if not CompanyID == 1:
            query = f"SELECT * FROM Companies WHERE CompanyID = {CompanyID}"
            rows = self._dict_query(query)
            # Returned in rows
            for row in rows:
                company["Exists"] = row["Exists"]
                company["Founded"] = row["Founded"]
            StartDate = company["Founded"]
            Today = datetime.datetime.today()
            diff = Today - StartDate
            company["Age"] = diff.days
        return company
    
    def Get_Incidents(self,company):
        """Returns a list of incidents for a given company"""
        query = f"SELECT Incident.IncidentDate from Incident CROSS JOIN Incidents CROSS JOIN Companies WHERE Companies.name = '{company}'"
        incidents = self._dict_query(query)
        return incidents

    def Get_Outage(self,market):
        """Returns true if the market has previously been registered for an outage"""
        query = "SELECT COUNT(RequestID) FROM FailedRequests WHERE Domain = (Select Domain from Marketplace WHERE name = %s) AND EndTime IS NULL"
        outage = self._list_query(query,[market])
        return outage

    def Finish_Outage(self,market,enddate):
        """Close out an opened outage"""
        query = "UPDATE FailedRequests SET EndTime = %s WHERE Domain = (Select Domain from Marketplace WHERE name = %s)"
        self._simple_query(query,(enddate,market))
    
    def Set_Outage(self,market,startdate):
        """Sets the start of an outage for a given domain"""
        query = "INSERT INTO FailedRequests(Domain,StartTime) VALUES ((Select Domain from Marketplace WHERE name = %s),%s)"
        self._simple_query(query,(market,startdate))
        return
    
    def Update_CompanyScore(self,market,Tcompany):
        """Update database with new CompanyScore"""
        print(f"New Company Score {Tcompany} for {market}")
        query = f"UPDATE Marketplace SET CompanyScore = {int(Tcompany)} WHERE MarketID={market.id}"
        self._simple_query(query)
        return

    def Update_DomainScore(self,market,Tdomain):
        """Update database with new DomainScore"""
        print(f"New Domain Score {Tdomain} for {market}")
        query = f"UPDATE Marketplace SET DomainScore = {int(Tdomain)} WHERE MarketID={market.id}"
        self._simple_query(query)
        return
    
    def Update_MarketScore(self,market,Tmarket):
        """Update database with new MarketScore"""
        print(f"New Market Score {Tmarket} for {market}")
        query = f"UPDATE Marketplace SET MarketScore = {int(Tmarket)} WHERE MarketID={market.id}"
        self._simple_query(query)
        return

    def Add_Certificate(self,domain,certificate,fingerprint):
        """Add a found certificate to the database"""
        print(f"New Certificate {domain},{fingerprint}")
        query = "INSERT INTO Certificate(CertificateType,fingerprint,FullCertificate) VALUES('SSL',%s,%s)"
        try:
            self._simple_query(query,(bytes(fingerprint),bytes(certificate)))
        except:
            pass
        return

    def Add_Application(self,app):
        """Add a found application to the database"""
        """Application is a dict of name, ismalware,sha1sum etc"""
        print(f"New Application {app['pkg_name']},{app['isMalware']}")
        addedtime = datetime.date.today()
        query = "INSERT into Applications(PackageName,Version,isMalware,MD5Sum,SHA1Sum,SHA256Sum,AppDate,AddedDate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        self._simple_query(query,(app["pkg_name"],app["Version_Name"],app["isMalware"],app["md5sum"],app["sha1sum"],app["sha256sum"],app["AppDate"],addedtime))
        return

    def Add_Available(self,MarketClass,Result):
        query = f"INSERT INTO Availability(ApplicationID,MarketID) VALUES((SELECT ApplicationID FROM Applications WHERE SHA256Sum = %s AND MD5Sum = %s),%s);"
        self._simple_query(query,(Result["sha256sum"],Result["md5sum"],MarketClass.id))
        return
    
    def Check_Exists(self, result):
        """Checks the result dict against the database"""
        query = "SELECT * FROM Applications WHERE SHA256Sum = %s AND MD5Sum = %s"
        results = self._list_query(query,(result['sha256sum'],result['md5sum']))
        if len(results) > 0:
            return True
        else:
            return False

    def _simple_query(self,*args,**kwargs):
        """Wrapper for simple query"""
        if self.db == None:
            self.Connect()
        cursor = self.db.cursor()
        cursor.execute(*args,**kwargs)
        cursor.close()
        self.Disconnect()
        return

    def _list_query(self,*args,**kwargs):
        """Wrapper for list queries"""
        if self.db == None:
            self.Connect()
        cursor = self.db.cursor()
        cursor.execute(*args,**kwargs)
        rows = cursor.fetchall()
        cursor.close()
        self.Disconnect()
        return rows
    
    def _dict_query(self,*args,**kwargs):
        """Wrapper for dict queries"""
        if self.db == None:
            self.Connect()
        cursor = self.db.cursor(my.cursors.DictCursor)
        cursor.execute(*args,**kwargs)
        rows = cursor.fetchall()
        cursor.close()
        self.Disconnect()
        return rows
