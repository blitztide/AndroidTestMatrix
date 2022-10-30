from signal import Handlers
import requests
import time
from AndroidTrustMatrix.Downloader import Plain_Get
from ppadb.client import Client as AdbClient
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

import AndroidTrustMatrix.config as Config
import AndroidTrustMatrix.adb as adb

install_x = 500
install_y = 500
prompt_x = 580
prompt_y = 802
home_x = 61
home_y = 1304
installable_color = (1,2,3)
prompt_color = (1,2,3)


def Search(app):
    """Search for app in store and return True if available"""
    url = f"https://www.amazon.co.uk/s?k={app}"
    proxies = Config.get_proxy_config()
    useragent = Config.get_user_agent()
    headers = {
        "User-Agent": useragent,
        "Accept-Language": "en-US,en;q=0.5" # Attempt to ensure english language for parsing
    }
    search_response = Plain_Get(url,proxies=proxies,headers=headers)
    
    if not search_response.status_code == 200:
        print(f"Server error: {search_response.status_code} for app {app}")
        return False
    
    soup = BeautifulSoup(search_response.text,'html.parser')
    # look for s-search-result
    search_results = soup.findAll('div',attrs={'data-component-type':'s-search-result'})
    for search_result in search_results:
        #find value of data-asin field
        if not search_result.has_attr('data-asin'):
            # Not valid search result
            continue
        # Check if the search result if of 'App' type
        div = search_result.find('div',attrs={"class":"s-price-instructions-style"})
        if div == None:
            # Div could not be found
            continue
        # Only the App type has a-text-bold for the first 'A'
        a = div.find('a', attrs={"class":"a-text-bold"})
        if a == None:
            # A Not found
            continue
        if not a.text.strip() == "App":
            # Somehow not an app
            continue

        # Get new page information
        new_page = "https://www.amazon.co.uk" + a['href']
        item_response = Plain_Get(new_page,proxies=proxies,headers=headers)
        if not item_response.status_code == 200:
            print(f"Server error: {item_response.status_code} for page {a['href']}")
            continue # Check next item
        item_soup = BeautifulSoup(item_response.content,'html.parser')
        item_result = item_soup.findAll('meta',attrs={'bundle-id':app})
        if item_result == None:
            # The app is not here!
            continue
        # Check app for price
        price_result = item_soup.find('strong', attrs={'class':'priceLarge'})
        if price_result == None:
            # Price not found
            continue
        if not price_result.text.strip() == "Free Download":
            print(f"App found but price is: {price_result.contents.strip()}")
            return False
        # Our app exists and is free
        return True
    return False

def check_installable(image):
    """Checks a BytesIO object for presence of install button"""
    file = Image.open(image)
    rgb_image = file.convert('RGB')
    #button can be in one of two places
    button_positions = [(500,500),(600,500)]
    for position in button_positions:
        r,g,b = rgb_image.getpixel(position)
        #Check if the button is present
        if r==0 and g == 202 and b == 255:
            return position
    return None

def Download(app):
    """Downloads the app and returns a file object, None on error"""
    # Connect to adb server
    host,port = Config.get_adb_config()
    client = AdbClient(host,port)
    # check all devices for app
    app_location = None
    devices = client.devices()
    
    # Handle no devices available
    if devices == []:
        return None
    for device in devices:
        if device.is_installed(app):
            print(f"{device} has {app}")
            app_location = device
    #if not found, force install
    if app_location == None:
        device = devices[0]
        adb.unlock(device)
        adb.home(device)
        amazon_intent = f"am start -a android.intent.action.VIEW -d 'amzn://apps/android?p={app}'"
        device.shell(amazon_intent)
        time.sleep(5)
        screenshot = device.screencap()
        installable = check_installable(BytesIO(screenshot))
        if not installable:
            adb.lock(device)
            print(f"App: {app} not installable on device: {device.serial}")
            return None
        adb.click(device,install_x,install_y)
        install_prompt = adb.get_focused(adb.get_activities(device))
        while not install_prompt == "com.android.packageinstaller.PackageInstallerActivity":
            install_prompt = adb.get_focused(adb.get_activities(device))
            time.sleep(5)
        adb.click(device,prompt_x,prompt_y)
        # Should be installing now, reset screen
        adb.click(device,home_x,home_y) # Reset store to home
        adb.home(device) # Set device to homescreen
        adb.lock(device)
        # Wait for app to properly install
        adb.waitinstall(device,app)
       
    # Extract file from phone
    adb.download_apk(device,app)

    # Load file into memory
    file = open(Config.get_temp_apk_path(),"rb")
    apk = file.read()
    file.close()
    return apk

def isUP():
    """Does a simple web request to see if service is up"""
    url = f"https://www.amazon.co.uk"
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