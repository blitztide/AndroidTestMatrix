import requests
from bs4 import BeautifulSoup

import AndroidTrustMatrix.Tests.Markets.mkt_googleplay as gp

def Name():
    return "Google Play Price Check"



def Run():
    apps = ["com.termux","ca.hamaluik.timecop"]
    for app in apps:
        gp.Search(app)