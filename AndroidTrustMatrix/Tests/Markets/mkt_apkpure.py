url = "https://apkpure.com/search?q={}"

def Search(app):
    """Search for app in store and return True if available"""
    print("Unable to Download, Cloudflare")
    return False

def Download(app):
    """Downloads the app and returns a file object, None on error"""
    return None

def isUP():
    """Does a simple web request to see if service is up"""
    return True

if __name__ == "__main__":
    import hashlib
    app = "com.termux"
    if Search(app):
        apk = Download(app)
        md5sum = hashlib.md5(apk).digest()
        print(f"Filehash: {md5sum}")