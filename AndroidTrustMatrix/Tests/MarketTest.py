from AndroidTrustMatrix.Tests import BaseTest
class MarketTest(BaseTest):
    """Class for holding and running Market Tests"""
    def __init__(self,db):
        super(MarketTest,self).__init__(db)
    
    def Run(self, Market):
        print(f"Running MarketTest on {Market}")