import requests
from AndroidTrustMatrix.Downloader import Plain_Head

import AndroidTrustMatrix.config as Config

def Search(app):
    """Search for app in store and return True if available"""
    print("Unimplemented")
    return False

def Download(app):
    """Downloads the app and returns a file object, None on error"""
    return None

def isUP():
    """Does a simple web request to see if service is up"""
    url = "https://appgallery.huawei.com"
    proxies = Config.get_proxy_config()
    useragent = Config.get_user_agent()
    headers = {
        "User-Agent": useragent
    }
    try:
        Plain_Head(url,proxies=proxies,headers=headers,timeout=5)
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