import os

import Hector


class dbHelper:

    def __init__(self):
        self.database = Hector.conf.database.Database()

    def prepareDB(self):
        self.database.createIfNotExists()
        self.database.setDefaultValues()
