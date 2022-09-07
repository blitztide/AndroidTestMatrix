import datetime
import os
import time
import AndroidTrustMatrix.config as Config

def unlock(device):
    # Check if asleep
    is_on = get_screenstate(device)
    if not is_on:
        device.shell("input keyevent 26")
        time.sleep(1)
        device.shell("input swipe 367.5 1171 367.5 1171 2000")
    return

def lock(device):
    is_on = get_screenstate(device)
    if is_on:
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

def Market_App(device,app,store):
    command = f"am start -a android.intent.action.VIEW -d 'market://details?id={app}' {store}"
    device.shell(command)

def waitinstall(device,app):
    found = device.is_installed(app)
    counter = 0
    while found == False:
        # break at 1 minutes
        if counter == 600:
            print(f"Unwilling to wait longer than 5 minutes for app {app}")
            return False
        time.sleep(1)
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
    print(f"app path {path}")
    downloaded = False
    while not downloaded == True:
        try:
            #print(f"{downloaded}Attempting Download")
            #print(f"{path} -> {Config.get_temp_apk_path()}")
            # Appears to be broken
            device.pull(path,Config.get_temp_apk_path())
            #command = f"adb pull '{path}' '{Config.get_temp_apk_path()}'"
            #os.system(command)
        except Exception as e:
            print(f"ADB pull failed {e}, trying again")
        downloaded = True

def remove(device,app):
    command = f"pm uninstall {app}"
    device.shell(command)

def hello(device):
    result = device.shell("echo hello")
    return result.strip()

def get_activities(device):
    result = device.shell("dumpsys activity activities")
    return result

def get_focused(appstring):
    # Check for mCurrentFocus in activitylist
    for line in appstring.splitlines():
        if line.strip()[0:13] == "mCurrentFocus":
            # Extract app name
            return line.strip().split('/')[-1][:-1]
    return None