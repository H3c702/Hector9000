# drinks_more_recipes.py
from Hector9000.conf import database as DB
drink_list = [
    {
        "name": "Extra Schuss Mate",
        "recipe": [("ingr", "mate", 50)]
    }, {
        "name": "Moscow Mule",
        "recipe": [
            ("ingr", "vodka", 60),
            ("ingr", "lime", 10),
            ("ingr", "gibe", 180)
        ]
    }, {
        "name": "Gin & Tonic",
        "color": "white",
        "recipe": [
            ("ingr", "gin", 40),
            ("ingr", "tonic", 120),
        ]
    }, {
        "name": "Screwdriver",
        "color": "orange",
        "recipe": [
            ("ingr", "vodka", 40),
            ("ingr", "oj", 120),
            ("stir", True),
        ]
    }, {
        "name": "Virgin Sunrise",
        "color": "red",
        "recipe": [
            ("ingr", "oj", 140),
            ("ingr", "gren", 15),
            ("umb", True),
        ]
    }, {
        "name": "Tequila Sunrise",
        "color": "darkred",
        "recipe": [
            ("ping", True),
            ("ingr", "tequila", 50),
            ("ping", True),
            ("ingr", "oj", 150),
            ("shake", True),
            ("ingr", "gren", 15),
            ("umb", True),
        ]
    },
    {
        "name": "Tschunk",
        "recipe": [
            ("ingr", "rum", 40),
            ("ingr", "mate", 120)
        ]
    }, {
        "name": "Caipirinha",
        "recipe": [
            ("ingr", "rum", 40),
            ("ingr", "gga", 120)
        ]
    }, {
        "name": "Gin and Sin",
        "recipe": [
            ("ingr", "gin", 35),
            ("ingr", "lime", 20),
            ("ingr", "gren", 5),
            ("ingr", "oj", 40)
        ]
    }, {
        "name": "Horny Bull",
        "recipe": [
            ("ingr", "tequila", 20),
            ("ingr", "oj", 120)
        ]
    }, {
        "name": "Monkey Gland",
        "recipe": [
            ("ingr", "gin", 30),
            ("ingr", "oj", 40),
            ("ingr", "gren", 5)
        ]
    }, {
        "name": "Margarita",
        "recipe": [
            ("ingr", "vodka", 20),
            ("ingr", "oj", 120)
        ]
    }, {
        "name": "Shirley Temple",
        "recipe": [
            ("ingr", "gga", 100),
            ("ingr", "gren", 5)
        ]
    }, {
        "name": "Raspberry Zero",
        "recipe": [
            ("ingr", "oj", 160),
            ("ingr", "pine", 60),
            ("ingr", "gren", 20)
        ]
    }, {
        "name": "Raspberry Pi",
        "recipe": [
            ("ingr", "oj", 140),
            ("ingr", "pine", 60),
            ("ingr", "gren", 20),
            ("ingr", "vodka", 20)
        ]
    }
]

actions = {
    # code      text     is_automatic?
    "ingr": ("Add Ingredient", True),
    "ping": ("Ring Bell", True),
    "shake": ("Shake", False),
    "stir": ("Stir", False),
    "ice": ("Add Ice", False),
    "umb": ("Add Umbrella", False),
}


myDB = DB.Database()

available_ingredients = myDB.get_Servos_asList()
ingredients = myDB.get_AllIngredientsAsDict()


def doable(drink, available):
    return False not in [ing in available for ing in [step[1]
                                                      for step in drink["recipe"] if step[0] == "ingr"]]


def alcoholic(drink):
    return True in [ingredients[step[1]][1]
                    for step in drink["recipe"] if step[0] == "ingr"]


available_drinks = [
    drink for drink in drink_list if doable(
        drink, available_ingredients)]
