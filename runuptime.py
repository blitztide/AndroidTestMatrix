#!/usr/bin/env python3
import time
from datetime import datetime

from AndroidTrustMatrix.util import ImportModule
import AndroidTrustMatrix.db
import AndroidTrustMatrix.config as Config
import TOR.tor as TOR

class UptimeEngine():
    """Main runner for Uptime Engine"""
    def __init__(self):
        """Initialise access to database and find marketplace names"""
        print("Initialising DB")
        username,password,host,port,database = Config.get_db_config()
        self.db = AndroidTrustMatrix.db.db()
        self.db.Connect(username,password,host,port,database)
        self.Markets = self.db.Get_Markets()
        self.tor_ip,self.tor_port,self.tor_pass = Config.get_tor_admin()
        self.proxies = Config.get_proxy_config()

    def checkup(self,market,market_module):
        # Get current down value in market
        currently_down = int(self.db.Get_Outage(market.name)[0][0])
        
        # Check if it is actually up
        Today = datetime.today()
        if market_module.isUP() == True:
            if currently_down:
                # Add end date for value
                print(f"{Today} {market.name} Outage over")
                self.db.Finish_Outage(market.name,Today)
            return True
        else:
            if not currently_down:
                print(f"{Today} {market.name} Outage Start")
                self.db.Set_Outage(market.name,Today)
            return False
        

    def run(self):
        print("Starting uptime engine")
        while True:
            # Forever loop
            down_count = 0    
            for market in self.Markets:
                # Load market module
                market_module = ImportModule(market)
                is_up = self.checkup(market,market_module)
                if not is_up:
                    down_count += 1
                del(market_module)
            if down_count > 2:
                print("Too many failed requests, cycling TOR")
                TOR.main(self.tor_ip,self.tor_port,self.tor_pass)
                time.sleep(10)
                print(TOR.getnewip(self.proxies))
                self.db.Rollback()
            else:
                self.db.Flush()
            time.sleep(10)

        

if __name__ == "__main__":
    app = UptimeEngine()
    app.run()