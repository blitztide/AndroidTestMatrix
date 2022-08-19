class Marketplace():
    def __init__(self,id,name,Domain,Company):
        self.name = name
        self.id = id
        self.domain = Domain
        self.Company = Company
    def __repr__(self):
        return self.name
