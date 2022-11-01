import AndroidTrustMatrix.Tests.Markets.mkt_uptodown as u2d
# Default test to ensure that the test framework runs
def Name():
    return "Uptodown"

def Run():
    u2d.Search("com.amazon.kindle")
    u2d.Search("com.termux")
    u2d.Download("com.amazon.kindle")
    return