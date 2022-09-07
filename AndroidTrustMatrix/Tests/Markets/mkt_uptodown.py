from bs4 import BeautifulSoup, NavigableString
import requests
import re

import AndroidTrustMatrix.config as Config
from AndroidTrustMatrix.Downloader import Plain_Head, Plain_Post, Progress_Download,Plain_Get


def Search(app):
    """Search for app in store and return True if available"""
    # Initial search for app
    url = "https://en.uptodown.com/android/search"
    search = url.format(app)
    proxies = Config.get_proxy_config()
    useragent = Config.get_user_agent()
    headers = {
        "User-Agent": useragent
    }
    data = {
        "q" : app
    }
    response = requests.post(search,proxies=proxies,headers=headers,data=data)
    if not response.status_code == 200:
        return False
    soup = BeautifulSoup(response.text,'html.parser')
    # Find the item list
    itemlist = soup.find("div",attrs={"id":"content-list"})
    if itemlist == None:
        return False
    itemlist.find_all("div",attrs={"class":"item"})

    # Iterate over search results
    for item in itemlist:
        #Trim location.href and trailing quote
        if isinstance(item,NavigableString):
            # Not an item we are looking for
            continue

        if not item.has_attr('onclick'):
            # Not the item we are searching for
            continue
        new_url = item.attrs['onclick'][15:-1]
        # Check if new page is the actual app page
        potential_app = Plain_Get(new_url,proxies=proxies,headers=headers)
        soup = BeautifulSoup(potential_app.text,'html.parser')
        section = soup.find("section",attrs={"class":"info","id":"technical-information"})
        table = section.find("tr",attrs={"class":"full"})
        # Select second data item in table
        package_name = table.find_all("td")[1].text
        if package_name == app:
            print(f"located package: {app}")
            return True
    print(f"Unable to locate package: {app}")
    return False

def Download(app):
    """Downloads the app and returns a file object, None on error"""
    # Initial search for app
    url = "https://en.uptodown.com/android/search"
    search = url.format(app)
    proxies = Config.get_proxy_config()
    useragent = Config.get_user_agent()
    headers = {
        "User-Agent": useragent
    }
    data = {
        "q" : app
    }
    response = Plain_Post(search,proxies=proxies,headers=headers,data=data)
    if not response.status_code == 200:
        return None
    soup = BeautifulSoup(response.text,'html.parser')
    # Find the item list
    itemlist = soup.find("div",attrs={"id":"content-list"})
    if itemlist == None:
        return None
    itemlist.find_all("div",attrs={"class":"item"})

    # Iterate over search results
    for item in itemlist:
        #Trim location.href and trailing quote
        if isinstance(item,NavigableString):
            # Not an item we are looking for will not have attrs
            continue

        new_url = item.attrs['onclick'][15:-1]
        # Check if new page is the actual app page
        potential_app = Plain_Get(new_url,proxies=proxies,headers=headers)
        soup = BeautifulSoup(potential_app.text,'html.parser')
        section = soup.find("section",attrs={"class":"info","id":"technical-information"})
        table = section.find("tr",attrs={"class":"full"})
        # Select second data item in table
        package_name = table.find_all("td")[1].text
        if package_name == app:
            print(f"located package: {app}")
            break
    if not package_name == app:
        return None
    download_page = new_url + '/download'
    response = Plain_Get(download_page,proxies=proxies,headers=headers)
    download_soup = BeautifulSoup(response,'html.parser')
    button = download_soup.find('button',attrs={"id":"detail-download-button","class":"button download"})
    download_url = button['data-url']
    
    if download_url:
        print(f"Downloading {app} from Uptodown")
        response = Progress_Download(download_url,proxies=proxies,headers=headers)
        return response
    return None

def isUP():
    """Does a simple web request to see if service is up"""
    url = "https://en.uptodown.com/android"
    proxies = Config.get_proxy_config()
    useragent = Config.get_user_agent()
    headers = {
        "User-Agent": useragent
    }
    try:
        requests.head(url,proxies=proxies,headers=headers,timeout=5)
        return True
    except:
        return False

if __name__ == "__main__":
    import hashlib
    app = "com.termux"
    if Search(app):
        apk = Download(app)
        md5sum = hashlib.md5(apk).digest()
        print(f"Filehash: {md5sum}")