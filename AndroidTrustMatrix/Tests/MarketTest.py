import importlib
from re import T
from AndroidTrustMatrix.Tests import BaseTest
from AndroidTrustMatrix.Tests.MalwareTest import MalwareTest
from AndroidTrustMatrix.util import eprint
import AndroidTrustMatrix.config as Config

class MarketTest(BaseTest):
    """Class for holding and running Market Tests"""
    def __init__(self,db,applist):
        super(MarketTest,self).__init__(db)
        self.searchapps = applist
        self.availableapps = [] # List of pkg_names
        self.proxy = Config.get_proxy_config()
    
    def Run(self, Market):
        print(f"Running MarketTest on {Market}")
        # Load Module for market
        self.market = Market
        MarketModule = self.ImportModule(Market)
        if MarketModule != None:
            # Check if market is up
            isUP = MarketModule.isUP()
            if isUP:
                # Check availability
                Tavail = self.CalculateAvailability(MarketModule)
                Tmalware = self.MalwareCheck(MarketModule)
                Tuptime = self.CalculateUptime(Market)
                Tmarket = self.CalculateScore(Tuptime,Tavail,Tmalware)
                self.db.Update_MarketScore(Market,Tmarket)
            #Unload module
            del(MarketModule)

    
    def ImportModule(self,Market):
        """Dynamically import market modules"""
        # print(f"Loading Module mkt_{Market}")
        marketstring = Market.__str__().strip().replace(" ","")
        importstr = f"AndroidTrustMatrix.Tests.Markets.mkt_{marketstring}"
        try:
            module = importlib.import_module(importstr)
            return module
        except:
            eprint(f"Unable to import {importstr}")
        return None

    def CalculateAvailability(self,MarketClass):
        # appcount = 0
        # For application in applicationlist:
        #   exists = module[Market].search()
        #   appcount += exists
        # Tavail = appcount/TotalApps
        # return Tavail
        appcount = 0
        totalapps = 0
        for application in self.searchapps:
            totalapps += 1
            if MarketClass.Search(application):
                self.availableapps.append(application)
                appcount += 1
        Tavail = appcount/totalapps
        return Tavail

    def MalwareCheck(self, MarketClass):
        # foreach apk in self.availableapps
        # Download()
        #   Run Malware engine on file
        # Calculate percentage of applications with malware
        # Return Tmalware
        malwaretest = MalwareTest(self.db,self.availableapps)
        Checked = 0
        Malicious = 0
        Tmalware = 0
        for application in self.availableapps:
            Checked += 1
            apk = MarketClass.Download(application)
            if apk != None:
                Result = malwaretest.Run(apk)
                Result["pkg_name"] = application
                exists = self.db.Check_Exists(Result)
                if not exists:
                    self.db.Add_Application(Result)
                if Result["isMalware"]:
                    print(f"Package {Result['pkg_name']} detected as Malicious")
                    Malicious += 1
                else:
                    print(f"Package {Result['pkg_name']} detected as Clean")
                self.db.Add_Available(self.market,Result)
        try:
            Tmalware = 1 - (Malicious/Checked)
        except:
            Tmalware = 0
        return Tmalware

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
        a = 3
        b = 3
        c = 4
        Tmarket = (a*Tuptime)+(b*Tavailability)+(c*Tmalware)
        return Tmarket
