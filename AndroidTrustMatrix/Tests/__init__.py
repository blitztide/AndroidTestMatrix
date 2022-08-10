import math
class BaseTest():
    def __init__(self, db):
        self.db = db
        self.k =  0.0030099
        self.Thalf = 1095
    def Run(self):
        print("Running Test")
    def Sigmoid(self,t):
        T = 1/ (1 + math.exp(self.k - (t - self.Thalf)))
        return T