from AndroidTrustMatrix.util import AndroidXMLDecompress
import glob
import zipfile

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