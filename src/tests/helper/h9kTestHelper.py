import os

import Hector


class dbHelper:
    def __init__(self, dbname):
        self.dbname = dbname

    def prepareDB(self):
        self.removeDB()
        self.database = Hector.conf.database.Database(self.dbname)
        self.database.createIfNotExists()
        self.database.setDefaultValues()

    def removeDB(self):
        if os.path.exists(self.dbname + ".db"):
            os.remove(self.dbname + ".db")
