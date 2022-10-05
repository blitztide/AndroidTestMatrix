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
        self.db = AndroidTrustMatrix.db.db()
        self.Markets = self.db.Get_Markets()
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
                TOR.main()
                time.sleep(10)
                TOR.getnewip(self.proxies)
            time.sleep(60)

        

if __name__ == "__main__":
    app = UptimeEngine()
    app.run()