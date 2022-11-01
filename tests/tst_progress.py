from AndroidTrustMatrix.Downloader import Progress_Download
# Testing progress download
def Name():
    return "Progress"

def Run():
    url = "http://speedtest.ftp.otenet.gr/files/test1Mb.db"
    file = Progress_Download(url)
    assert len(file) == 1048576
    return