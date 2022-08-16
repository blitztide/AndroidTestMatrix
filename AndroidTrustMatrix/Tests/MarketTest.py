from re import T
from AndroidTrustMatrix.Tests import BaseTest
class MarketTest(BaseTest):
    """Class for holding and running Market Tests"""
    def __init__(self,db):
        super(MarketTest,self).__init__(db)
        self.availableapps = [] # List of pkg_names
    
    def Run(self, Market):
        db = self.db
        print(f"Running MarketTest on {Market}")
        # Load Module for market
        MarketModule = self.ImportModule(Market)
        # Check availability
        Tavail = self.CalculateAvailability(MarketModule)
        Tmalware = self.MalwareTest(MarketModule)
        Tuptime = self.CalculateUptime(Market)
        Tmarket = self.CalculateScore(Tuptime,Tavail,Tmalware)
        db.Update_MarketScore(Market,Tmarket)
        #Unload module
        del(MarketModule)

    
    def ImportModule(self,Market):
        print(f"Loading Module mkt_{Market}")
        importstr = f"mkt_{Market}"
        try:
            module = __import__(importstr)
            return module
        except:
            print(f"Unable to import {importstr}")
        return None

    def CalculateAvailability(self,MarketClass):
        # Search for top 1000 apps:
        # appcount = 0
        # For application in applicationlist:
        #   exists = module[Market].search()
        #   appcount += exists
        # Tavail = appcount/TotalApps
        # return Tavail
        return 0

    def MalwareTest(self, MarketClass):
        # foreach apk in self.availableapps
        # Download()
        #   Check filehash
        #   Lookup in our own database (if found tag as such)
        #   If not found, check VT
        #   If not found, check ClamAV
        #   If not found, upload to VT
        #   Check VT again
        #   Tag application in database
        # Calculate percentage of applications with malware
        # Return Tmalware
        return 0

    def CalculateUptime(self,market):
        db = self.db
        # Get all downtime events
        # For loop through downtime events since project start
        # Calculate lazy percentage
        totaltime = 100
        actualtime = 100
        Tuptime = actualtime/totaltime
        return Tuptime

    def CalculateScore(self,Tuptime,Tavailability,Tmalware):
        a = 0
        b = 0
        c = 0
        Tmarket = (a*Tuptime)+(b*Tavailability)+(c*Tmalware)
        return Tmarket