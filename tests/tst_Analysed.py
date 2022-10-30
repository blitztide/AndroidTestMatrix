import AndroidTrustMatrix.db
# Test to ensure the DB analysed recently function works
def Name():
    return "db Analysed_recently"

def Run():
    # Test known
    db = AndroidTrustMatrix.db.db()
    market = "fdroid"
    app = "com.termux"
    result = db.Analysed_Recently(market,app)
    assert result == False

    # Test unknown
    market = "aaabbb"
    app = "cccddd"
    result = db.Analysed_Recently(market,app)
    assert result == False
    return