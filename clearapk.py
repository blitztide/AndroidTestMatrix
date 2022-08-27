#!/usr/bin/env python3
from ppadb.client import Client as AdbClient

import AndroidTrustMatrix.config as Config
import AndroidTrustMatrix.adb as adb

def should_delete(package):
    return False

def run():
    host,port = Config.get_adb_config()
    client = AdbClient(host,port)
    devices = client.devices()
    for device in devices:
        packages = str.splitlines(device.shell("pm list packages"))
        for package in packages:
            #Check if it is in packages.list
            pkg_name = package[8:]
            print(pkg_name)
            if should_delete(pkg_name):
                device.shell(f"pm uninstall {pkg_name}")


if __name__ == "__main__":
    run()
