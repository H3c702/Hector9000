import pytest

from tests.helpers import h9kTestHelper


class Test_database:
	dbhelper = h9kTestHelper.dbHelper()

	@pytest.fixture(autouse=True)
	def run_around_tests(self):
		# Code that will run before your test, for example:
		self.dbhelper.prepareDB()
		# A test function will be run at this point
		yield
		# Code that will run after your test, for example:
		self.dbhelper.resetDB()
		# assert files_before == files_after

	def test_GetServos(self):
		servos = self.dbhelper.database.get_Servos()

		assert len(servos) == 12

	def test_GetServosAsList(self):
		servos = self.dbhelper.database.get_Servos_asList()
		assert "['gren', 'rum', 'vodka', 'gin', 'tequila', 'gibe', 'lime', 'tonic', 'mate', " \
			   "'gga', 'pine', 'oj']" == str(servos)

	@pytest.mark.parametrize("servo, code", [(1, "gren"), (2, "rum")])
	def test_Get_Servo(self, servo, code):
		servo = self.dbhelper.database.get_Servo(servo)

		assert servo == code

	@pytest.mark.parametrize("servo, code", [(1, "oj"), (2, "gibe")])
	def test_Set_Servo(self, servo, code):
		item = self.dbhelper.database.set_Servo(servo, code)

		assert item == code

	def test_addIngredient(self):
		self.dbhelper.database.add_Ingredient("abcd", "Abcdefg", 1)
		ing = self.dbhelper.database.get_AllIngredientsAsDict()

		assert "{'gin': ('Gin', True), 'rum': ('Rum', True), 'vodka': ('Vodka', True), 'tequila': ('Tequila', True), " \
		   "'tonic': ('Tonic Water', False), 'coke': ('Cola', False), 'oj': ('Orange Juice', False), " \
		   "'gren': ('Grenadine', False), 'mmix': ('Margarita Mix', True), 'mate': ('Mate', False), " \
		   "'pine': ('Pineapple Juice', False), 'raspberry': ('Raspberry', False), 'gga': ('Ginger Ale', False), " \
		   "'cocos': ('Cocos', False), 'mango': ('Mango Juice', False), 'lms': ('Limettensaft', False), " \
		   "'coin': ('Cointreau', True), 'lime': ('Lime', False), 'gibe': ('Ginger Beer', False), 'abcd': ('Abcdefg', True)}" == str(ing)

	def test_deleteIIngredient(self):
		self.dbhelper.database.delete_Ingredient("gin")
		ing = self.dbhelper.database.get_AllIngredientsAsDict()
		assert "{'rum': ('Rum', True), 'vodka': ('Vodka', True), 'tequila': ('Tequila', True), " \
			   "'tonic': ('Tonic Water', False), 'coke': ('Cola', False), 'oj': ('Orange Juice', False), " \
			   "'gren': ('Grenadine', False), 'mmix': ('Margarita Mix', True), 'mate': ('Mate', False), " \
			   "'pine': ('Pineapple Juice', False), 'raspberry': ('Raspberry', False), 'gga': ('Ginger Ale', False), " \
			   "'cocos': ('Cocos', False), 'mango': ('Mango Juice', False), 'lms': ('Limettensaft', False), " \
			   "'coin': ('Cointreau', True), 'lime': ('Lime', False), 'gibe': ('Ginger Beer', False)}" == str(ing)

	def test_GetIngredients(self):
		ing = self.dbhelper.database.get_AllIngredients()

		assert ing[0][1] == "Gin"

	def test_get_AllIngredientsAsDict(self):
		ing = self.dbhelper.database.get_AllIngredientsAsDict()
		print(ing)
		assert "{'gin': ('Gin', True), 'rum': ('Rum', True), 'vodka': ('Vodka', True), 'tequila': ('Tequila', True), " \
			   "'tonic': ('Tonic Water', False), 'coke': ('Cola', False), 'oj': ('Orange Juice', False), " \
			   "'gren': ('Grenadine', False), 'mmix': ('Margarita Mix', True), 'mate': ('Mate', False), " \
			   "'pine': ('Pineapple Juice', False), 'raspberry': ('Raspberry', False), 'gga': ('Ginger Ale', False), " \
			   "'cocos': ('Cocos', False), 'mango': ('Mango Juice', False), 'lms': ('Limettensaft', False), " \
			   "'coin': ('Cointreau', True), 'lime': ('Lime', False), 'gibe': ('Ginger Beer', False)}" == str(ing)

	def test_count_up_ingredient(self):
		self.dbhelper.database.countUpIngredient("Gin", 200)

		ingrcount = self.dbhelper.database.get_Ingredients_Log()
		assert len(ingrcount) == 1

	def test_count_up_Drinks(self):
		self.dbhelper.database.countUpDrink("Mate")

		drinkCount = self.dbhelper.database.get_Drinks_Log()
		assert len(drinkCount) == 1

	@pytest.mark.parametrize("setting, value", [("cupsize", 400)])
	def test_get_settings(self, setting, value):
		item = int(self.dbhelper.database.get_Setting(setting))

		assert item == value

	@pytest.mark.parametrize("setting, value", [("cupsize", "20")])
	def test_set_settings(self, setting, value):
		item = self.dbhelper.database.set_Setting(setting, value)

		assert item == value


	# ---------------------------------------------------------------------

	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.dbhelper.removeDB()
