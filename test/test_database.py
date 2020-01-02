from conf.database import Database
import os


class Test_databasees():
    dbname = "temp"
    database = Database(dbname)

    def test_GetServos(self):
        self.prepareDB()
        servos = self.database.get_Servos()

        assert len(servos) == 12

    def test_GetServosAsList(self):
        self.prepareDB()
        servos = self.database.get_Servos_asList()
        assert "['oj', 'tequila', 'gren', 'vodka', 'mmix', 'rum', 'coke', 'gin', 'tonic', 'mate', 'rum', 'pine']" == str(servos)

    def test_GetIngredients(self):
        self.prepareDB()

        ing = self.database.get_AllIngredients()

        assert ing[0][1] == "Gin"

    # ---------------------------------------------------------------------

    def prepareDB(self):
        self.removeDB()
        self.database = Database(self.dbname)
        self.database.createIfNotExists()
        self.database.setDefaultValues()

    def removeDB(self):
        if os.path.exists(self.dbname + ".db"):
            os.remove(self.dbname + ".db")

    def __exit__(self):
        self.removeDB()
