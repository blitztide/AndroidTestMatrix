import requests
import json
from io import BytesIO
from AndroidTrustMatrix.Downloader import Plain_Get, Progress_Download
import AndroidTrustMatrix.config as Config


url = "http://ws75.aptoide.com/api/7/apps/search/query={}/limit=3"

def Search(app):
    """Search for app in store and return True if available"""
    search = url.format(app)
    proxies = Config.get_proxy_config()
    useragent = Config.get_user_agent()
    headers = {
        "User-Agent": useragent
    }
    response = Plain_Get(search,proxies=proxies,headers=headers)
    if response.status_code == 200:
        jdata = json.loads(response.text)
        results = jdata['datalist']
        for item in results['list']:
            if item['package'] == app:
                print(f"Located package: {app}")
                return True
    print(f"Unable to locate package: {app}")
    return False

def Download(app):
    """Downloads the app and returns a file object, None on error"""
    search = url.format(app)
    proxies = Config.get_proxy_config()
    useragent = Config.get_user_agent()
    headers = {
        "User-Agent": useragent
    }
    response = Plain_Get(search,proxies=proxies,headers=headers)
    downloadurl=None
    if response.status_code == 200:
        jdata = json.loads(response.text)
        results = jdata['datalist']
        for item in results['list']:
            if item['package'] == app:
                downloadurl = item['file']['path']
    if downloadurl:
        print(f"Downloading {app} from Aptoide")
        response2 = Progress_Download(downloadurl,proxies=proxies,headers=headers)
        return response2
    else:
        return None

def isUP():
    """Does a simple web request to see if service is up"""
    search = url.format("com.sec.android.app.popupcalculator")
    proxies = Config.get_proxy_config()
    useragent = Config.get_user_agent()
    headers = {
        "User-Agent": useragent
    }
    try:
        requests.get(search,proxies=proxies,headers=headers,timeout=5)
        return True
    except:
        return False

if __name__ == "__main__":
    import hashlib
    app = "com.sec.android.app.popupcalculator"
    if Search(app):
        apk = Download(app)
        md5sum = hashlib.md5(apk).hexdigest()
        print(f"Filehash: {md5sum}")