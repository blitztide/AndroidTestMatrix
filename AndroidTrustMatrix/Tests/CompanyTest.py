from AndroidTrustMatrix.Tests import BaseTest
class CompanyTest(BaseTest):
    """Class for holding and running Company Tests"""
    def __init__(self,db):
        super(CompanyTest,self).__init__(db)
        #Modify these to Adjust sigmoid
        #self.k =  0.0030099
        #self.Thalf = 1095

    def Run(self,Market):
        print(f"Running CompanyTest on {Market}")
        db = self.db
        company = db.Get_CompanyInfo(Market)
        if( company["Exists"]==True):
            incidents = db.Get_Incidents(company)
            Tincidents = self.Test_Incidents(incidents)
        else:
            Tincidents = 0
        (Treg,Tage) = self.Test_Registered(company)
        Tcompany = self.Calculate_Score(Treg,Tage,Tincidents)
        db.Update_CompanyScore(Market,Tcompany)
        

    def Calculate_Score(self,Treg,Tage,Tincident):
        Tcompany = Tincident * ( (5 * Treg)+(5*Tage))
        return Tcompany
    
    def Test_Registered(self,company):
        if (company["Exists"]):
            Treg = 5
            Tage = self.Sigmoid(company["Age"])
        else:
            Treg = 0
            Tage = 0
        return Treg,Tage
    
    def Test_Incidents(self,incidents):
        return 0
    