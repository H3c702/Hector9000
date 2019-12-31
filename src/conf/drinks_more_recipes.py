# drinks_more_recipes.py
drink_list = [
        { "name": "Extra Schuss Mate",
            "recipe":[("ingr", "mate", 75)]},
         {
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
                            "name": "Margarita-T",
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
                                        },
                                {
                                        "name": "Tschunk",
                                        "alc": True,
                                        "recipe": [
                                            ("ingr", "rum", 40),
                                            ("ingr", "mate", 200)
                                            ]
                                        }, {
                                             #   "name": "Virgin Sunrise",
                                              #  "recipe": [
                                               #     ("ingr", "oj", 150),
                                               #     ("ingr", "gren", 15)
                                                #    ]
                                              #  }, {
                                               #         "name": "Tequila Sunrise",
                                                #        "recipe": [
                                                 #           ("ingr", "tequila", 50),
                                                  #          ("ingr", "oj", 150),
                                                   #         ("ingr", "gren", 15)
                                                    #        ]   
                                                     #   }, {
                                                                "name": "Bacardi Cocktail",
                                                                "recipe": [
                                                                    ("ingr, ""rum", 45),
                                                                    ("ingr", "lms", 20),
                                                                    ("ingr", "gren", 10)
                                                                    ]   
                                                                }, {
                                                                        "name": "Boyarskiy",
                                                                        "recipe": [
                                                                            ("ingr", "gren", 25),
                                                                            ("ingr", "vodka", 25)
                                                                            ]   
                                                                        }, {
                                                                                "name": "Rum Buck",
                                                                                "recipe": [
                                                                                    ("ingr","rum", 50),
                                                                                    ("ingr","gga", 100)
                                                                                    ]   
                                                                                }, {
                                                                                        "name": "Caipirinha",
                                                                                        "recipe": [
                                                                                            ("ingr","cachaca", 50)
                                                                                            ]   
                                                                                        }, {
                                                                                                "name": "Caipioska",
                                                                                                "recipe": [
                                                                                                    ("ingr", "vodka", 50)
                                                                                                    ]   
                                                                                                }, {
                                                                                                        "name": "Chupacabra",
                                                                                                        "recipe": [
                                                                                                            ("ingr", "tequila", 50)
                                                                                                            ]   
                                                                                                        }, {
                                                                                                                "name": "Cuba Libre",
                                                                                                                "recipe": [
                                                                                                                    ("ingr","rum", 70),
                                                                                                                    ("ingr", "coke", 140),
                                                                                                                    ("ingr", "lms", 3)
                                                                                                                    ]   
                                                                                                                }, {
                                                                                                                        "name": "Gimlet",
                                                                                                                        "recipe": [
                                                                                                                            ("ingr", "gin", 60),
                                                                                                                            ("ingr", "lms", 15)
                                                                                                                            ]   
                                                                                                                        }, {
                                                                                                                                "name": "Gin and Sin",
                                                                                                                                "recipe": [
                                                                                                                                    ("ingr", "gin", 30),
                                                                                                                                    ("ingr", "lms", 30),
                                                                                                                                    ("ingr", "gren", 2),
                                                                                                                                    ("ingr", "oj", 30)
                                                                                                                                    ]   
                                                                                                                                }, {
                                                                                                                                        "name": "Horny Bull",
                                                                                                                                        "recipe": [
                                                                                                                                            ("ingr", "tequila", 30),
                                                                                                                                            ("ingr", "oj", 350)
                                                                                                                                            ]   
                                                                                                                                        }, {
                                                                                                                                                "name": "Horny Bull Shot",
                                                                                                                                                "recipe": [
                                                                                                                                                    ("ingr", "tequila", 20),
                                                                                                                                                    ("ingr", "rum", 20),
                                                                                                                                                    ("ingr", "vodka", 20)
                                                                                                                                                    ]   
                                                                                                                                                }, {
                                                                                                                                                        "name": "Kamikaze",
                                                                                                                                                        "recipe": [
                                                                                                                                                            ("ingr", "vodka", 30),
                                                                                                                                                            ("ingr", "coin", 30),
                                                                                                                                                            ("ingr", "lms", 30)
                                                                                                                                                            ]   
                                                                                                                                                        }, {
                                                                                                                                                                "name": "Margarita Special",
                                                                                                                                                                "recipe": [
                                                                                                                                                                    ("ingr", "tequila", 50),
                                                                                                                                                                    ("ingr", "coin", 30),
                                                                                                                                                                    ("ingr", "lms", 10)
                                                                                                                                                                    ]   
                                                                                                                                                                }, {
                                                                                                                                                                        "name": "Monkey Gland",
                                                                                                                                                                        "recipe": [
                                                                                                                                                                            ("ingr", "gin", 50),
                                                                                                                                                                            ("ingr", "oj", 30),
                                                                                                                                                                            ("ingr", "gren", 3)
                                                                                                                                                                            ]   
                                                                                                                                                                        }, {
                                                                                                                                                                                "name": "Roy Rogers",
                                                                                                                                                                                "recipe": [
                                                                                                                                                                                    ("ingr", "gren", 8),
                                                                                                                                                                                    ("ingr", "coke", 30)
                                                                                                                                                                                    ]   
                                                                                                                                                                                }, {
                                                                                                                                                                                        "name": "Margarita-V",
                                                                                                                                                                                        "recipe": [
                                                                                                                                                                                            ("ingr", "vodka", 50),
                                                                                                                                                                                            ("ingr","oj", 100)
                                                                                                                                                                                           ]   
                                                                                                                                                                                        }, {
                                                                                                                                                                                                "name": "Shirley Temple",
                                                                                                                                                                                                "recipe": [
                                                                                                                                                                                                    ("ingr", "gga", 180),
                                                                                                                                                                                                    ("ingr", "gren", 4)
                                                                                                                                                                                                    ]   
                                                                                                                                                                                                }, {
                                                                                                                                                                                                        "name": "Long Island \nIced Tea",
                                                                                                                                                                                                        "recipe": [
                                                                                                                                                                                                            ("ingr", "vodka", 15),
                                                                                                                                                                                                            ("ingr", "tequila", 15),
                                                                                                                                                                                                            ("ingr","rum", 15),
                                                                                                                                                                                                            ("ingr", "gin", 15),
                                                                                                                                                                                                            ("ingr", "lms", 10),
                                                                                                                                                                                                            ("ingr","coke", 50)
                                                                                                                                                                                                            ]   
                                                                                                                                                                                                        },
                                                                                                                                                                                                {
                                                                                                                                                                                                        "name": "Raspberry Zero",
                                                                                                                                                                                                        "recipe": [
                                                                                                                                                                                                            ("ingr", "oj", 200),
                                                                                                                                                                                                            ("ingr", "pine", 80),
                                                                                                                                                                                                            ("ingr", "raspberry", 20)
                                                                                                                                                                                                            ]
                                                                                                                                                                                                        },
                                                                                                                                                                                                {
                                                                                                                                                                                                        "name": "Raspberry Pi",
                                                                                                                                                                                                        "recipe": [
                                                                                                                                                                                                            ("ingr", "oj", 180),
                                                                                                                                                                                                            ("ingr", "pine", 80),
                                                                                                                                                                                                            ("ingr", "raspberry", 20),
                                                                                                                                                                                                            ("ingr", "vodka", 20)
                                                                                                                                                                                                            ]
                                                                                                                                                                                                        },{"name":"Extra Schuss Cola",
                                                                                                                                                                                                                "recipe":[("ingr", "coke", 75)]}
                                                                                                                                                                                                ]


#-> Read out of DB
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
        "pine": ("Pineapple Juice", False),
        "raspberry": ("Raspberry", False),
        "gga": ("Ginger Ale", False),
        "cocos": ("Cocos", False),
        "mango": ("Mango Juice", False),
        "lms": ("Limettensaft", False),
        "coin": ("Cointreau", True)
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


# To DB -> replace
available_ingredients = ["gren", "coin", "lms", "oj", "mate", "gin", "vodka", "tequila", "rum", "raspberry", "coke", "pine"]

def doable(drink, available):
    return False not in [ing in available for ing in [step[1] for step in drink["recipe"] if step[0] == "ingr"]]


def alcoholic(drink):
    return True in [ingredients[step[1]][1] for step in drink["recipe"] if step[0] == "ingr"]





#print("doable:")
#for drink in drink_list:    print(drink["name"], doable(drink, available_ingredients))

available_drinks = [drink for drink in drink_list if doable(drink, available_ingredients)]


#print("available:")
#for d in available_drinks:
#    print(d["name"] + " (" + ("" if alcoholic(d) else "non-") + "alcoholic)")
