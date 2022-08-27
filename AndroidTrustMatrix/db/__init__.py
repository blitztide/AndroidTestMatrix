import datetime
import MySQLdb as my
import AndroidTrustMatrix.Marketplaces as MP

class db():
    """db class abstracts all db functionality"""

    def Connect(self,username, password, host, port, database):
        """Initialise connection to database"""
        self.db = my.connect(host,username,password,database)
        print(f'Connected: {username}@{host}:{port}/{database}')

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
            URI = row["URI"]
            if "Company" in row.keys():
                Company = row["Company"]
            else:
                Company = 0

            markets.append(MP.Marketplace(MarketID,name,URI,Company))
        return markets
    
    def Get_CompanyInfo(self,market):
        """Extracts all relevant Company Information for a given Market to return as a dict"""
        company = {}
        company["Exists"] = False
        CompanyID = market.Company
        if not CompanyID == None:
            query = f"SELECT * FROM Companies WHERE CompanyID = {CompanyID}"
            rows = self._dict_query(query)
            for row in rows:
                company["Exists"] = row["Exists"]
                company["Founded"] = row["Founded"]
            dateformat = "%Y-%m-%d %H:%M:%S"
            StartDate = datetime.strptime(company["Founded"],dateformat)
            Today = datetime.today().strftime(dateformat)
            diff = Today - StartDate
            company["Age"] = diff.days
        return company
    
    def Get_Incidents(self,company):
        """Returns a list of incidents for a given company"""
        query = f"SELECT IncidentDate FROM Incidents WHERE Company = {company}"
        incidents = self._dict_query(query)
        return incidents
    
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
        cursor = self.db.cursor()
        cursor.execute(*args,**kwargs)
        cursor.close()
        return

    def _list_query(self,*args,**kwargs):
        """Wrapper for list queries"""
        cursor = self.db.cursor()
        cursor.execute(*args,**kwargs)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    
    def _dict_query(self,*args,**kwargs):
        """Wrapper for dict queries"""
        cursor = self.db.cursor(my.cursors.DictCursor)
        cursor.execute(*args,**kwargs)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def Disconnect(self):
        """Close connection to database"""
        if(self.db):
            self.db.close()
    
    def __del__(self):
        if (self.db):
            self.db.commit()
            self.db.close()
