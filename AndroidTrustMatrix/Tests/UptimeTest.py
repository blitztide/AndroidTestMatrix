from AndroidTrustMatrix.Tests import BaseTest
import AndroidTrustMatrix.config as Config

class UptimeTest(BaseTest):
    """Class for holding and running Market Tests"""
    def __init__(self,db):
        super(UptimeTest,self).__init__(db)
        self.proxy = Config.get_proxy_config()

    def run():
        pass