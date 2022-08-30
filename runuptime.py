#!/usr/bin/env python3
import time
from datetime import datetime

from AndroidTrustMatrix.util import ImportModule
import AndroidTrustMatrix.db
import AndroidTrustMatrix.config as Config

class UptimeEngine():
    """Main runner for Uptime Engine"""
    def __init__(self):
        """Initialise access to database and find marketplace names"""
        print("Initialising DB")
        username,password,host,port,database = Config.get_db_config()
        self.db = AndroidTrustMatrix.db.db()
        self.db.Connect(username,password,host,port,database)
        self.Markets = self.db.Get_Markets()

    def checkup(self,market,market_module):
        # Get current down value in market
        currently_down = self.db.Get_Outage('googleplay')[0][0]
        # Check if it is actually up
        Today = datetime.today()
        if market_module.isUP() == True:
            if currently_down:
                # Add end date for value
                print(f"{market.name} Outage over")
                self.db.Finish_Outage(market.domain,Today)
            return True
        else:
            if not currently_down:
                print(f"{market.name} Outage Start")
                self.db.Set_Outage(market.domain,Today)
            return False
        

    def run(self):
        print("Starting uptime engine")
        while True:
            # Forever loop    
            for market in self.Markets:
                # Load market module
                market_module = ImportModule(market)
                self.checkup(market,market_module)
                del(market_module)
            time.sleep(10)

        

if __name__ == "__main__":
    app = UptimeEngine()
    app.run()