from ppadb.client import Client as AdbClient
from PIL import Image
from io import BytesIO

import AndroidTrustMatrix.config as Config
import AndroidTrustMatrix.adb as adb

def Name():
    return "ADB"

def Run():
    host,port = Config.get_adb_config()
    client = AdbClient(host,port)
    devices = client.devices()
    for device in devices:
        print(f"Testing device: {device.serial}")
        assert adb.hello(device) == "hello"
        adb.unlock(device)
        assert adb.get_screenstate(device) == True
        adb.home(device)
        result = device.screencap()
        image = Image.open(BytesIO(result))
        adb.lock(device)
        assert adb.get_screenstate(device) == False
        
    return