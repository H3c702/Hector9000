import Hector.HectorController as HectorController

Controller = HectorController.HectorController()


class Test_Controller:

    def test_GetDrinksAsJSON(self):
        jsonfile = Controller.available_drinks_as_JSON()

        assert jsonfile == '{"drinks": [{"name": "Extra Schuss Mate", "id": 1, "alcohol": false}, {"name": "Moscow Mule", "id": 2, "alcohol": true}, {"name": "Gin & Tonic", "id": 3, "alcohol": true}, {"name": "Screwdriver", "id": 4, "alcohol": true}, {"name": "Virgin Sunrise", "id": 5, "alcohol": false}, {"name": "Tequila Sunrise", "id": 6, "alcohol": true}, {"name": "Tschunk", "id": 7, "alcohol": true}, {"name": "Caipirinha", "id": 8, "alcohol": true}, {"name": "Gin and Sin", "id": 9, "alcohol": true}, {"name": "Horny Bull", "id": 10, "alcohol": true}, {"name": "Monkey Gland", "id": 11, "alcohol": true}, {"name": "Margarita", "id": 12, "alcohol": true}, {"name": "Shirley Temple", "id": 13, "alcohol": false}, {"name": "Raspberry Zero", "id": 14, "alcohol": false}, {"name": "Raspberry Pi", "id": 15, "alcohol": true}]}'

    def test_Get_DrinkByID(self):
        msg = message()
        msg.payload = 5

        drink = Controller._get_drink_as_JSON(msg)
        print(drink)
        assert drink == '{"id": 5, "name": "Virgin Sunrise", "ingredients": [{"name": "Orange Juice", "ammount": 140}, {"name": "Grenadine", "ammount": 15}]}'


class message():
    def __init__(self):
        self.payload = "0"
        self.topic = "topic"
