import pytest

import src.HectorController

Controller = src.HectorController.HectorController()


def test_GetDrinksAsJSON():
    jsonfile = Controller.available_drinks_as_JSON()

    assert jsonfile == '{"drinks": [{"name": "Mate DDDD", "id": 1, "alcohol": false}, {"name": "Mate Quickie", "id": 2, "alcohol": false}, {"name": "Rum & Coke", "id": 3, "alcohol": true}, {"name": "Gin & Tonic", "id": 4, "alcohol": true}, {"name": "Screwdriver", "id": 5, "alcohol": true}, {"name": "Margarita", "id": 6, "alcohol": true}, {"name": "Virgin Sunrise", "id": 7, "alcohol": false}, {"name": "Tequila Sunrise", "id": 8, "alcohol": true}]}'


def test_Get_DrinkByID():
    drink = Controller.get_drink_as_JSON(2-1)

    assert drink == '{"name": "Mate Quickie", "color": "gold", "recipe": [["ingr", "mate", 50]]}'

