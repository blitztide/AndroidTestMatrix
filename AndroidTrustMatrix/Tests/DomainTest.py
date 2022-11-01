import re
import socket
import datetime
import dns.resolver
from datetime import datetime

from AndroidTrustMatrix.Tests import BaseTest
from AndroidTrustMatrix.Tests.CryptoTest import CryptoTest

class DomainTest(BaseTest):
    """Class for holding and running Domain Tests"""
    def __init__(self,db):
        super(DomainTest,self).__init__(db)
        #Modify these to Adjust sigmoid
        #self.k =  0.0030099
        #self.Thalf = 1095
    
    def Run(self, Market):
        db = self.db
        print(f"Running DomainTest on {Market}")
        protocol = re.findall("https?",Market.domain)[0]
        domain = re.findall(":\/\/([A-Za-z0-9\-\.]+)",Market.domain)[0]
        Tage = self.CheckAge(domain)
        Tcrypto = 0
        if(protocol == "https"):
            Tcrypto = self.CheckSSL(domain)
        Tc2 = self.CheckC2(domain)
        Tdomain = self.CalculateScore(Tc2,Tcrypto,Tage)
        print(f"{Market} Tc2: {Tc2} Tcrypto: {Tcrypto} Tage: {Tage} Tdomain: {Tdomain}")
        db.Update_DomainScore(Market,Tdomain)
    
    def CheckSSL(self,domain):
        test = CryptoTest(self.db)
        Tssl = test.run(domain)
        return Tssl

    def CheckAge(self,domain):
        whois = self.Whois(domain)
        
        for line in whois.splitlines():
            if line[0:7] == "created":
                Created = datetime.strptime(line[9:].strip(),"%Y-%m-%d")
                break
            if line[0:13] == "Creation Date":
                Created = datetime.strptime(line[14:].strip(),"%Y-%m-%dT%H:%M:%S%Z")
        Age = 0
        if (Created):
            Unixtime = datetime.strptime("1985-01-01","%Y-%m-%d")
            Today = datetime.today()
            diff = Today - Unixtime
            unixage = diff.days
            diff = Today - Created
            Age = diff.days
            if Age == unixage:
                print(f"Domain: {domain} is private, or as old as Unixtime!")
        Tage = self.Sigmoid(Age)
        
        return Tage

    def CalculateScore(self,Tc2,Tcrypto,Tage):
        # Scaling factors
        a = 5
        b = 5
        Tdomain = Tc2 * ((a * Tage) + (b*Tcrypto))
        return Tdomain
    
    def CheckC2(self,domain):
        """Simple check if quad-9 returns value"""
        resolver = dns.resolver.Resolver()
        resolver.nameservers=['9.9.9.9']
        try:
            # resolve raises exception if cannot resolve
            answer = resolver.resolve(domain,"A")
            return 1
        except:
            return 0


    def Whois(self, Domain):
        connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connection.connect(("whois.iana.org",43))
        connection.send(Domain.encode("ASCII") + b'\r\n')
        output = b""
        while 1:
            data = connection.recv(1024)
            if not data:
                break
            output = output + data
        connection.close()
        return output.decode()
