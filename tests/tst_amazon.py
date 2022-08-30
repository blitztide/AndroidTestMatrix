import AndroidTrustMatrix.Tests.Markets.mkt_googleplay as az
# Default test to ensure that the test framework runs
def Name():
    return "Amazon"

def Run():
    az.Search("com.king.candycrushsodasaga")
    az.Search("com.termux")
    return