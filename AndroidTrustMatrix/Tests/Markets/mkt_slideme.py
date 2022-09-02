import requests
from bs4 import BeautifulSoup
from AndroidTrustMatrix.Downloader import Progress_Download
import AndroidTrustMatrix.config as Config


baseurl = "http://slideme.org"
url = f"{baseurl}/applications/"
basesearch = url + "{}"
proxies = {"http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"}
headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }


def Search(app):
    """Search for app in store and return True if available"""
    searchurl = basesearch.format(app)
    print(f"Searching: {searchurl}")
    response = requests.get(searchurl,proxies=proxies,headers=headers)
    if response.status_code == requests.status_codes.codes.ok:
        soup = BeautifulSoup(response.text,'html.parser')
        searchresults = soup.find("div",{"class":"node-mobileapp"})
        if searchresults:
            apps = searchresults.find("a")
            print(baseurl + apps['href'])
            return True
        else:
            return False

def Download(app):
    """Downloads the app and returns a file object, None on error"""
    searchurl = basesearch.format(app)
    print(f"Searching: {searchurl}")
    downloadurl = None
    response = requests.get(searchurl,proxies=proxies,headers=headers)
    if response.status_code == requests.status_codes.codes.ok:
        soup = BeautifulSoup(response.text,'html.parser')
        searchresults = soup.find("div",{"class":"node-mobileapp"})
        if searchresults:
            apps = searchresults.find("a")
            apppage = baseurl + apps['href']
            response = requests.get(apppage,proxies=proxies,headers=headers)
            if response.status_code == requests.status_codes.codes.ok:
                soup = BeautifulSoup(response.text,'html.parser')
                downloaddiv = soup.find("div",{"class":"download-button"})
                downloadurl = downloaddiv.find("a")["href"]

    if downloadurl:
        print(f"Downloading {app} from SlideME")
        response = Progress_Download(downloadurl,proxies=proxies,headers=headers)
        return response
    return None

def isUP():
    """Does a simple web request to see if service is up"""
    url = "http://slideme.org"
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
    app = "com.twitter.android"
    if Search(app):
        apk = Download(app)
        if apk:
            md5sum = hashlib.md5(apk).digest()
            print(f"Filehash: {md5sum}")