from AndroidTrustMatrix.util import CheckVT
def Name():
    return "Test Virustotal detections"

def Run():
    test1 = CheckVT("d68daaf3b237f3ba386a0ae6a2e1cf56f8cbeb39f618ea44e9417b3a6717c6cc")
    if test1 != True:
        raise AssertionError(f"Known malicious not detected")
    test2 = CheckVT("8c93a6ed7326e2d21ba2b6ca58a2792b9202525f48b1b3707baf76b12ed86982")
    if test2 != False:
        raise AssertionError(f"Known clean detected, or unknown")

if __name__ == "__main__":
    Run()