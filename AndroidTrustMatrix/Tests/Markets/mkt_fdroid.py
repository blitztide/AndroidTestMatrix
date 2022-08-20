import os
import requests
import datetime
from io import BytesIO
import zipfile
import json

repodir = "/UNI/Repo"
fdroiddir= f"{repodir}/F-Droid"
repopath = f"{fdroiddir}/index-v1.json"
url = "https://f-droid.org/repo/index-v1.jar"
proxies = {"http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050"}
headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
jdata = ""
json_data = ""

def get_repolist():
    print("Updating fdroid repo")
    response = requests.get(url,stream=True,proxies=proxies,headers=headers)
    if response.status_code == requests.status_codes.codes.ok:
        zp = zipfile.ZipFile(BytesIO(response.content))
        fp = open(repopath,"wb")
        fp.write(zp.open("index-v1.json").read())
        fp.close()
    return

def should_update():
    #Check if repo exists
    #Creates if not
    if not os.path.exists(fdroiddir):
        os.mkdir(fdroiddir)
        return True
    if not os.path.exists(repopath):
        return True
    filetime = datetime.datetime.fromtimestamp(os.path.getmtime(repopath))
    # if older than 7 days, update
    today = datetime.datetime.today()
    diff = today-filetime
    if diff.days > 7:
        return True
    # File exists and is within 7 days
    return False

def search_local(app):
    found = False
    global json_data
    global jdata
    if json_data == "":
         json_data = open(repopath)
         jdata = json.load(json_data)
    try:
        jdata["packages"][app]
        found = True
    except:
        print(f"Unable to locate package: {app}")
        found = False

    return found

def get_download_name(app):
    global json_data
    global jdata
    try:
        jdata["packages"][app]
    except:
        print("Unable to locate package")
        return
    versions = []
    for version in jdata["packages"][app]:
        versions.append(f"{app}_{version['versionCode']}.apk")
    json_data.close()
    return versions[0]

def Search(app):
    """Search for app in store and return True if available. app = str(pkg_name)"""
    if should_update():
        get_repolist()
    if search_local(app):
        return True
    else:
        return False

def Download(app):
    """Downloads the app and returns a file object, None on error"""
    apk_name = get_download_name(app)
    url = f"https://f-droid.org/repo/{apk_name}"
    response = requests.get(url,proxies=proxies,headers=headers)
    if response.status_code == requests.status_codes.codes.ok:
        return response.content
    return None

def isUP():
    """Does a simple web request to see if service is up"""
    return True

if __name__ == "__main__":
    import hashlib
    app = "com.termux"
    if Search(app):
        apk = Download(app)
        
        if apk:
            md5sum = hashlib.md5(apk).hexdigest()
            print(f"Filehash: {md5sum}")

