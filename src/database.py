import sqlite3 as lite
import datetime
from time import *


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
        self.cur.execute("INSERT INTO IngredientsLog (ingredient, ml, date) VALUES (?, ?, ?)",
                         (ingredient, ml, datetime.datetime.now()))
        self.con.commit()

    def __del__(self):
        self.con.commit()
        self.con.close()


# when called directly, read out database and generate a log
if __name__ == "__main__":
    db = Database("h9k")
    db.cur.execute("SELECT * FROM DrinksLog WHERE date > '2018-12-11' ORDER BY date ASC")
    # db.cur.execute("SELECT * FROM DrinksLog ORDER BY date ASC")
    res = db.cur.fetchall()
    # print("%d entries" % len(res))
    for l in res:
        number, name, tstampstr = l
        tstamp = mktime(strptime(tstampstr.split(".")[0], "%Y-%m-%d %H:%M:%S"))
        tstamp += (14 * 24 * 3600 + 10 * 3600 + 8 * 60 + 28)
        print("%30s:  %s" % (strftime("%a %Y-%m-%d %H:%M:%S", localtime(tstamp)), name))
