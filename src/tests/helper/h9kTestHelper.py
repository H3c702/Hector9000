import os

import Hector


class dbHelper:

    def prepareDB(self):
        self.removeDB()
        self.database = Hector.conf.database.Database()
        self.database.createIfNotExists()
        self.database.setDefaultValues()

    def removeDB(self):
        if os.path.exists("h9k.db"):
            os.remove("h9k.db")
