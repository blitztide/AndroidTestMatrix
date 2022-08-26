import glob
import importlib
from math import e

class TestRunner():

    def __init__(self):
        self.tests = list()
        self.loadmodules()

    def Run(self):
        for test in self.tests:
            try:
                test.Run()
                print(f"Test {test.Name()} Passed")
            except Exception as e:
                print(f"Test {test.Name()} Failed {e}")

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

if __name__ == "__main__":
    TR = TestRunner()
    TR.Run()