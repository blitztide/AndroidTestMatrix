import AndroidTrustMatrix.db
import AndroidTrustMatrix.config as Config

class App():
    def __init__(self):
        print("Initialising DB")
        username,password,host,port,database = Config.get_db_config()
        self.db = AndroidTrustMatrix.db.db()
        self.db.Connect(username,password,host,port,database)
        self.Markets = self.db.Get_Markets()
        return

    def run(self):
        print("Running")
        print(self.Markets)

