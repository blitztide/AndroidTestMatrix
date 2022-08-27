import requests
from bs4 import BeautifulSoup

import AndroidTrustMatrix.Tests.Markets.mkt_googleplay as gp

def Name():
    return "Google Play Price Check"



def Run():
    apps = ["com.termux","ca.hamaluik.timecop"]
    # Check app is free and available
    test = gp.Search("com.termux")
    assert test == True
    # Check app is paid and available
    test = gp.Search("ca.hamaluik.timecop")
    assert test == False
    # Check app doesn't exist
    test = gp.Search("com.qweqwpoqweqweqwe.asdasdasd")
    assert test == False