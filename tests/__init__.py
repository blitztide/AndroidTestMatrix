import glob
import importlib
from math import e

class TestRunner():

    def __init__(self):
        self.tests = list()
        self.loadmodules()

    def Run(self):
        failcount = 0
        for test in self.tests:
            print(f"Starting Test {test.Name()}")
            try:
                test.Run()
                print(f"Test {test.Name()} Passed")
            except Exception as e:
                print(f"Test {test.Name()} Failed {e}")
                failcount += 1
        return failcount

    def loadmodules(self):
        """Dynamically import test modules into self.tests"""
        modules = list()
        testfiles = glob.glob("./tests/tst_*.py")

        for file in testfiles:
            # Remove ./ change / to . and remove .py
            modules.append(file[2:].replace("/",".")[0:-3])

        for test in modules:
                try:
                    module = importlib.import_module(test)
                    self.tests.append(module)
                except:
                    print(f"Unable to import {test}")
        return

def SingleTest(testfile):
    modulename = 'tests.' + testfile
    module = importlib.import_module(modulename,package=None)
    try:
        module.Run()
    except Exception as e:
        print(f"Test {module.Name()} Failed {e}")    

if __name__ == "__main__":
    TR = TestRunner()
    TR.Run()