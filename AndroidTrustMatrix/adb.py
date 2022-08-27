import datetime
import time
import AndroidTrustMatrix.config as Config

def unlock(device):
    device.shell("input keyevent 26")
    time.sleep(1)
    device.shell("input swipe 367.5 1171 367.5 1171 2000")
    return

def lock(device):
    device.shell("input keyevent 26")
    return

def get_screenstate(device):
    result = device.shell("dumpsys input_method | grep -o mInteractive=true")
    if result.strip() == "":
        return False
    else:
        return True

def home(device):
    device.shell("input keyevent 3")

def click(device,x,y):
    command = f"input touchscreen tap {x} {y}"
    device.shell(command)

def Market_App(device,app):
    command = f"am start -a android.intent.action.VIEW -d 'market://details?id={app}'"
    device.shell(command)

def waitinstall(device,app):
    found = device.is_installed(app)
    counter = 0
    while found == False:
        # break at 1 minutes
        if counter == 120:
            print(f"Unwilling to wait longer than 2 minutes for app {app}")
            return False
        time.sleep(5)
        found = device.is_installed(app)
        counter += 1
    return True
    

def get_app_path(device,app):
    location = device.shell(f"pm path {app}")
    path = None
    for line in location.splitlines():
        if line[-8:] == "base.apk":
            path = line[8:]
    return path

def download_apk(device,app):
    path = get_app_path(device,app)
    if path == None:
        return None
    device.pull(path,Config.get_temp_apk_path())

def remove(device,app):
    command = f"pm uninstall {app}"
    device.shell(command)

def hello(device):
    result = device.shell("echo hello")
    return result.strip()