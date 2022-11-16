from re import T
from AndroidTrustMatrix.Tests import BaseTest
from AndroidTrustMatrix.Tests.MalwareTest import MalwareTest
from AndroidTrustMatrix.util import eprint,ImportModule
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
        MarketModule = ImportModule(Market)
        if MarketModule != None:
            # Check if market is up
            isUP = MarketModule.isUP()
            if isUP:
                # Check availability
                Tavail = self.CalculateAvailability(MarketModule)
                Tmalware = self.MalwareCheck(MarketModule)
                Tuptime = self.CalculateUptime(Market)
                Tmarket = self.CalculateScore(Tuptime,Tavail,Tmalware)
                print(f"{Market} Tavail: {Tavail} Tmalware: {Tmalware} Tuptime: {Tuptime} Tmarket: {Tmarket}")
                self.db.Update_MarketScore(Market,Tmarket)
            #Unload module
            del(MarketModule)
        # Resetting Available Apps
        self.availableapps = []

    def CalculateAvailability(self,MarketClass):
        # DB lookup for each value
        # Tavail = appcount/TotalApps
        # return Tavail
        counter = 0
        for application in self.searchapps:
            print(f"Searching app {counter} of {len(self.searchapps)}")
            counter += 1
            # Check if it has been seen recently, to speed up subsequent runs
            seen = self.db.Analysed_Recently(self.market,application)
            if seen:
                self.availableapps.append(application)
                continue

            if MarketClass.Search(application):
                    self.availableapps.append(application)
        
        appcount = self.db.Get_Market_App_Count(self.market)
        totalapps = self.db.Get_Total_Apps()
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
        total_available = len(self.availableapps)
        counter = 0
        for application in self.availableapps:
            print(f"Analyzing app {counter} of {total_available}")
            Checked += 1
            counter += 1
            if self.db.Analysed_Recently(self.market,application):
                continue
            apk = MarketClass.Download(application)
            if apk != None:
                Result = malwaretest.Run(apk)
                Result["pkg_name"] = application
                Result["market"] = self.market
                exists = self.db.Check_Exists(Result)
                if not exists:
                    self.db.Add_Application(Result)
                if Result["isMalware"]:
                    print(f"Package {Result['pkg_name']} detected as Malicious")
                    Malicious += 1
                else:
                    # Have we already seen this available?
                    if self.db.Check_Available(Result):
                        print(f"Package {Result['pkg_name']} detected as Clean")
                    else:
                        pass
                self.db.Add_Available(self.market,Result)
            
        # Use DB to get counts
        Checked = self.db.Get_Market_App_Count(self.market)
        Malicious = self.db.Get_Market_Malware_Count(self.market)
        print(f"{self.market} has {Checked} Applications which {Malicious} are Malware")
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
        #db.get_FailedRequests(market)
        totaltime = 100
        actualtime = 100
        Tuptime = actualtime/totaltime
        return Tuptime

    def CalculateScore(self,Tuptime,Tavailability,Tmalware):
        a = 1
        b = 4
        c = 5
        Tmarket = (a*Tuptime)+(b*Tavailability)+(c*Tmalware)
        return Tmarket
