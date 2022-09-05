import AndroidTrustMatrix.adb as adb

def Name():
    return "Focus"

def Run():
    file1 = open("tests/testfiles/activities.1").read()
    assert adb.get_focused(file1) == "com.android.packageinstaller.PackageInstallerActivity"
    file2 = open("tests/testfiles/activities.2").read()
    assert adb.get_focused(file2) == "com.amazon.venezia.AppstoreReactNativeActivity"
    return