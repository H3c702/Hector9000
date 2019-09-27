import pytest

import src.HectorController

Controller = src.HectorController.HectorController()



def test_GetDrinksAsJSON():
    jsonfile = Controller.available_drinks_as_JSON()

    assert jsonfile == '{"drinks": [{"name": "Mate DDDD", "id": 1, "alcohol": false}, {"name": "Mate Quickie", "id": 2, "alcohol": false}, {"name": "Rum & Coke", "id": 3, "alcohol": true}, {"name": "Gin & Tonic", "id": 4, "alcohol": true}, {"name": "Screwdriver", "id": 5, "alcohol": true}, {"name": "Margarita", "id": 6, "alcohol": true}, {"name": "Virgin Sunrise", "id": 7, "alcohol": false}, {"name": "Tequila Sunrise", "id": 8, "alcohol": true}]}'


def test_Get_DrinkByID():

    msg = message()
    msg.payload = 5

    drink = Controller.get_drink_as_JSON(msg)
    print(drink)
    assert drink == '{"id": 5, "name": "Margarita", "ingredients": [{"name": "Tequila", "ammount": 50}, {"name": "Margarita Mix", "ammount": 150}]}'

class message():
    def __init__(self):
        self.payload = "0"
        self.topic = "topic"