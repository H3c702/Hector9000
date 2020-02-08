from conf.database import Database
import os


class Test_database:
    dbname = "temp"
    database = Database(dbname)

    def test_os(self):
        print(os.path)

    def test_GetServos(self):
        self.prepareDB()
        servos = self.database.get_Servos()

        assert len(servos) == 12

    def test_GetServosAsList(self):
        self.prepareDB()
        servos = self.database.get_Servos_asList()
        assert "['oj', 'tequila', 'gren', 'vodka', 'mmix', 'rum', 'coke', 'gin', 'tonic', 'mate', 'rum', 'pine']" == str(
            servos)

    def test_GetIngredients(self):
        self.prepareDB()

        ing = self.database.get_AllIngredients()

        assert ing[0][1] == "Gin"

    def test_count_up_ingredient(self):
        self.prepareDB()
        self.database.countUpIngredient("Gin", 200)

        ingrcount = self.database.get_Ingredients_Log()
        assert len(ingrcount) == 1

    def test_count_up_Drinks(self):
        self.prepareDB()
        self.database.countUpDrink("Mate")

        drinkCount = self.database.get_Drinks_Log()
        assert  len(drinkCount) == 1


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



