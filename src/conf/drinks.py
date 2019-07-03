# drinks.py
drink_list = [
    {
        "name": "Mate DDDD",
        "color": "gold",
        "recipe": [
            ("ingr", "mate", 50),
        ]
    },
    {
        "name": "Mate Quickie",
        "color": "gold",
        "recipe": [
            ("ingr", "mate", 50),
        ]
    }, {
        "name": "Rum & Coke",
        "color": "chocolate",
        "recipe": [
            ("ingr", "rum", 50),
            ("ingr", "coke", 150),
        ]
    }, {
        "name": "Gin & Tonic",
        "color": "white",
        "recipe": [
            ("ingr", "gin", 50),
            ("ingr", "tonic", 150),
        ]
    }, {
        "name": "Screwdriver",
        "color": "orange",
        "recipe": [
            ("ingr", "vodka", 50),
            ("ingr", "oj", 150),
            ("stir", True),
        ]
    }, {
        "name": "Margarita",
        "color": "gold",
        "recipe": [
            ("ingr", "tequila", 50),
            ("ingr", "mmix", 150),
            ("umb", True),
        ]
    }, {
        "name": "Virgin Sunrise",
        "color": "red",
        "recipe": [
            ("ingr", "oj", 150),
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
    }
]

ingredients = {
    # code				text		is_alcoholic?
    "gin": ("Gin", True),
    "rum": ("Rum", True),
    "vodka": ("Vodka", True),
    "tequila": ("Tequila", True),
    "tonic": ("Tonic Water", False),
    "coke": ("Coke", False),
    "oj": ("Orange Juice", False),
    "gren": ("Grenadine", False),
    "mmix": ("Margarita Mix", True),
    "mate": ("Mate", False),
}

actions = {
    # code      text     is_automatic?
    "ingr": ("Add Ingredient", True),
    "ping": ("Ring Bell", True),
    "shake": ("Shake", False),
    "stir": ("Stir", False),
    "ice": ("Add Ice", False),
    "umb": ("Add Umbrella", False),
}

# To DB -> replace Servo_config
available_ingredients = ["oj", "tequila", "gren", "vodka", "mmix", "rum", "coke", "gin", "tonic", "mate"]


def doable(drink, available):
    return False not in [ing in available for ing in [step[1] for step in drink["recipe"] if step[0] == "ingr"]]


def alcoholic(drink):
    return True in [ingredients[step[1]][1] for step in drink["recipe"] if step[0] == "ingr"]





print("doable:")
for drink in drink_list:    print(drink["name"], doable(drink, available_ingredients))

available_drinks = [drink for drink in drink_list if doable(drink, available_ingredients)]


print("available:")
for d in available_drinks:
    print(d["name"] + " (" + ("" if alcoholic(d) else "non-") + "alcoholic)")
