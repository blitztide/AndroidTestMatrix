import math
class BaseTest():
    def __init__(self, db):
        self.db = db
    def Run(self):
        print("Running Test")
    def Sigmoid(self,t):
        k =  0.0030099
        Thalf = 1095
        T = 1/ (1 + math.exp(k - (t - Thalf)))
        return T