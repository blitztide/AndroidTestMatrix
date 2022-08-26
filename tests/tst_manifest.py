from AndroidTrustMatrix.util import AndroidXMLDecompress
import glob
import zipfile
import re

def Name():
    return "manifest"

def Run():
    for file in glob.glob("./tests/testfiles/*.apk"):
        assert zipfile.is_zipfile(file)
        archive = zipfile.ZipFile(file)
        filelist = archive.namelist()
        if not "AndroidManifest.xml" in filelist:
            raise AssertionError("AndroidManifest.xml not found")
        manifestFile = archive.open("AndroidManifest.xml")
        decoder = AndroidXMLDecompress()
        manifest = decoder.decompressXML(manifestFile.read())
        package_regex = r'<manifest [^>]+package="([A-Za-z0-9\.-]+)"'
        version_regex = r'<manifest [^>]+versionName="([A-Za-z0-9\.-]+)"'
        search_package = re.search(package_regex,manifest)
        if search_package == None:
            raise AssertionError(f"search_package == None in {file}")
        search_version = re.search(version_regex,manifest)
        if search_version == None:
            raise AssertionError(f"search_version == None in {file}")
        print(search_package.group(1))
        print(search_version.group(1))