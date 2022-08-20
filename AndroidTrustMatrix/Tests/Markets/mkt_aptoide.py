import requests
import json
from io import BytesIO

url = "http://ws75.aptoide.com/api/7/apps/search/query={}/limit=3"
proxies = {"http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"}
headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }

def Search(app):
    """Search for app in store and return True if available"""
    search = url.format(app)
    response = requests.get(search,proxies=proxies,headers=headers)
    if response.status_code == 200:
        jdata = json.loads(response.text)
        results = jdata['datalist']
        for item in results['list']:
            if item['package'] == app:
                return True
    print(f"Unable to locate package: {app}")
    return False

def Download(app):
    """Downloads the app and returns a file object, None on error"""
    search = url.format(app)
    response = requests.get(search,proxies=proxies,headers=headers)
    downloadurl=None
    if response.status_code == 200:
        jdata = json.loads(response.text)
        results = jdata['datalist']
        for item in results['list']:
            if item['package'] == app:
                downloadurl = item['file']['path']
    if downloadurl:
        print(f"Downloading {app} from Aptoide")
        response2 = requests.get(downloadurl,proxies=proxies,headers=headers)
        if response2.status_code != 200:
            return None
        else:
            return response2.content
    else:
        return None

def isUP():
    """Does a simple web request to see if service is up"""
    return True

if __name__ == "__main__":
    import hashlib
    app = "com.termux"
    if Search(app):
        apk = Download(app)
        md5sum = hashlib.md5(apk).hexdigest()
        print(f"Filehash: {md5sum}")