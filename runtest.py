#!/usr/bin/env python3
import tests
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tests.SingleTest(sys.argv[1])
        
    else:
        TR = tests.TestRunner()
        value = TR.Run()
        if value == 0:
            print(f"All tests Passed!")
        else:
            print(f"{value} tests failed!")
            exit(value)
        exit()
