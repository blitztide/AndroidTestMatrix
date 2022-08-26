from PIL import Image
from AndroidTrustMatrix.Tests.Markets.mkt_googleplay import check_installbutton


def Name():
    return "images"

def Run():
    with Image.open("tests/testfiles/gp_1.png") as im:
        assert im.format == "PNG"
        test = check_installbutton(im)
        assert test == False
    with Image.open("tests/testfiles/gp_2.png") as im:
        assert im.format == "PNG"
        test = check_installbutton(im)
        assert test == True
    return