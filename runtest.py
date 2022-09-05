#!/usr/bin/env python3
import tests

if __name__ == "__main__":
    TR = tests.TestRunner()
    value = TR.Run()
    if value == 0:
        print(f"All tests Passed!")
    else:
        print(f"{value} tests failed!")
    exit(value)
