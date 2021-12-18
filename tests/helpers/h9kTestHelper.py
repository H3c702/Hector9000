import os

import Hector9000 as Hector


class dbHelper:

    def __init__(self):
        self.database = Hector.conf.database.Database()

    def prepareDB(self):
        self.resetDB()

        self.database.createIfNotExists()
        self.database.setDefaultValues()

    def resetDB(self):
        # self.database.cur.execute("DELETE FROM Drinks;")
        self.database.cur.execute("DELETE FROM settings;")
        self.database.cur.execute("DELETE FROM Servos;")
        self.database.cur.execute("DELETE FROM Ingredients;")
        # self.database.cur.execute("DELETE FROM Actions;")
        self.database.cur.execute("DELETE FROM DrinksLog;")
        self.database.cur.execute("DELETE FROM IngredientsLog;")

    def removeDB(self):
        os.remove("./h9k.db")
