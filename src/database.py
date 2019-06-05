import sqlite3 as lite
import datetime


class Database:
    con = None
    cur = None

    def __init__(self, dbname):
        self.con = lite.connect(dbname + ".db")
        self.cur = self.con.cursor()

    def createIfNotExists(self):
        self.cur.execute("CREATE TABLE if not exists DrinksLog(ID Integer primary key, drink TEXT, date timestamp)")
        self.cur.execute("CREATE TABLE if not exists IngredientsLog(ID Integer primary key, ingredient TEXT,"
                         "ml integer, date timestamp)")
        '''
        self.cur.execute("CREATE TABLE if not exists Ingredients (ID Integer primary key, name TEXT, nicename TEXT, "
                         "isalcoholic bool)")
        '''

        self.con.commit()

    def countUpDrink(self, drink):
        self.cur.execute("INSERT INTO DrinksLog (drink, date) VALUES (?, ?)", (drink, datetime.datetime.now()))
        self.con.commit()

    def countUpIngredient(self, ingredient, ml):
        self.cur.execute("INSERT INTO IngredientsLog (ingredient, ml, date) VALUES (?, ?, ?)", (ingredient, ml, datetime.datetime.now()))
        self.con.commit()

    def __del__(self):
        self.con.commit()
        self.con.close()
