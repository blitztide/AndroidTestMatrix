class Marketplace():
    def __init__(self,id,name,Domain):
        self.name = name
        self.id = id
        self.domain = Domain
    def __repr__(self):
        return self.name