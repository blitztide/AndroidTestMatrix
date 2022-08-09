from AndroidTrustMatrix.Tests import BaseTest
class DomainTest(BaseTest):
    """Class for holding and running Domain Tests"""
    def __init__(self,db):
        super(DomainTest,self).__init__(db)
    
    def Run(self, Market):
        print(f"Running MarketTest on {Market}")