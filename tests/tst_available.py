import AndroidTrustMatrix.db

# Test to ensure tha availability workaround works
def Name():
    return "Availability"

def Run():
    db = AndroidTrustMatrix.db.db()
    testresult = {
        "market": "fdroid",
        "pkg_name": "com.borneq.heregpslocation",
        "sha256sum": "c275a89ee02d4bd155c5783817833452a3ac70bcd2f0e13dc08f0fd31a3d8b27"
    }
    result = db.Check_Available(testresult)
    assert result
    return True