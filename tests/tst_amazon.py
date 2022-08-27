import AndroidTrustMatrix.Tests.Markets.mkt_googleplay as az
# Default test to ensure that the test framework runs
def Name():
    return "Amazon"

def Run():
    assert az.Search("com.king.candycrushsodasaga") == True
    assert az.Search("com.termux") == False
    return