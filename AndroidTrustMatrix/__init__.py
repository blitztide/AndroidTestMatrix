import signal

import AndroidTrustMatrix.db
import AndroidTrustMatrix.config as Config
import AndroidTrustMatrix.DomainTest as DomainTest
import AndroidTrustMatrix.CompanyTest as CompanyTest
import AndroidTrustMatrix.MarketTest as MarketTest

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
        return

    def run(self):
        """Start the application"""
        db = self.db
        print("Running")
        while True:
            for market in self.Markets:
                MarketTest.Run(market)
                DomainTest.Run(market)
                CompanyTest.Run(market)

    def __del__(self):
        print("Exiting")