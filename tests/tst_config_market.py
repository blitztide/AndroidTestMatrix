# Test to ensure market selection from config file
import AndroidTrustMatrix.config as Config

def Name():
    return "Market Config"

def Run():
    print(Config.get_markets())
    return