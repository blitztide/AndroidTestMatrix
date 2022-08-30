#!/usr/bin/env python3
import tests

if __name__ == "__main__":
    TR = tests.TestRunner()
    value = TR.Run()
    print(f"{value} tests failed!")
    exit(value)
