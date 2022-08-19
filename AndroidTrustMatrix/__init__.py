import signal
import random
from AndroidTrustMatrix.Tests.CompanyTest import CompanyTest
from AndroidTrustMatrix.Tests.DomainTest import DomainTest
from AndroidTrustMatrix.Tests.MarketTest import MarketTest

import AndroidTrustMatrix.db
import AndroidTrustMatrix.config as Config
from AndroidTrustMatrix.Tests import *

def handler(signum,frame):
    exit(1)

signal.signal(signal.SIGINT, handler)



class App():
    """Main app class for AndroidTrustMatrix"""
    def __init__(self):
        """Initialiser establishing connection to db and enumrating markets"""
        print("Initialising DB")
        username,password,host,port,database = Config.get_db_config()
        self.db = AndroidTrustMatrix.db.db()
        self.db.Connect(username,password,host,port,database)
        self.Markets = self.db.Get_Markets()
        self.appchecks = 10
        return

    def run(self):
        """Start the application"""
        db = self.db
        print("Running")
        apps = self.SelectApps(self.appchecks)
        markettest = MarketTest.MarketTest(db,apps)
        domaintest = DomainTest.DomainTest(db)
        companytest = CompanyTest.CompanyTest(db)
        for market in self.Markets:
            markettest.Run(market)
            domaintest.Run(market)
            companytest.Run(market)

    def SelectApps(self,n):
        """Select n random apps and return a list of pkg_names"""
        apps = []
        with open("config/apps") as fp:
            for line in fp:
                apps += line
        random.shuffle(apps)
        return [apps[0:n-1]]

    def __del__(self):
        print("Exiting")
