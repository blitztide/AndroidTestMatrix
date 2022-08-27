from PIL import Image
from io import BytesIO
from AndroidTrustMatrix.Tests.Markets.mkt_googleplay import check_installbutton


def Name():
    return "images"

def test(filepath):
    #Get file to be a series of bytes
    fp = open(filepath,"rb")
    file = fp.read()
    fp.close()
    image = Image.open(BytesIO(file))
    assert image.format == "PNG"
    test = check_installbutton(BytesIO(file))
    return test

def Run():
    assert test("./tests/testfiles/gp_1.png") == None
    assert test("./tests/testfiles/gp_2.png") == (576,585)
    return test("./tests/testfiles/gp_2.png") == (515,465)