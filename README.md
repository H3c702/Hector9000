HECTOR 9000
======================

Minimal Requirements 
---

	- RaspberryPi 3
	- Debian bases Linux (to use installscript)

Install on RaspberryPi
----
First you have to clone the github repo of Hector

	git clone https://github.com/H3c702/Hector9000.git

This repository doesn't contain a frontent. To get the original Hector9000 frontend see: 

	https://github.com/H3c702/Hector9000WebUI

To start the Hector software first move into the directory:

	cd Hector9000

Then run this command to setup all necessary tools:

	./setup.sh

To start the software run:

	./start.sh


Start Hector :

	cd Hector9000
	cd srv
	python3 main.py

Add Drinks
---

To add a new Drink you have to modify the `drinks.py` file and add a new item into the `drink_list` array formatted as followed:

	{
        "name": "NAME OF DRINK",
        "recipe": [
            ("ingr", "INGREDIENT1", AMOUNT1),
            ("ingr", "INGREDIENT2", AMOUNT2)
        ]	
    }

All strings in `UPPERCASE` are placeholders, all lowercase strings have to be used literally in the definition. The `INGREDIENTx` names are not cleartext but are identifiers referencing into the `ingredients` list below in the same file. The `AMOUNTx` values are numerical values of the corresponding ingredient's amount in grams.

At the moment there are only some ingredients but feel free to put in some new. You can add them freely to the dictionary.

	# "ID":("NAME", ISALCOHOLIC)
	ingredients = {
		"gin": ("Gin", True),
		"rum": ("Rum", True),
		"vodka": ("Vodka", True),
		"tequila": ("Tequila", True),
		"tonic": ("Tonic Water", False),
		"coke": ("Coke", False),
		"oj": ("Orange Juice", False),
		"gren": ("Grenadine", False),
		"mmix": ("Margarita Mix", True)
		...

Here each ingredient identifier is mapped into a tuple containing the NAME used in the UI and a flag that tells whether the ingredient contains alcohol.
A future extension might allow multi-language UIs.

Assigning valves
---

Because Hector has twelve valve channels you have twelve valves each mapped to one ingredient (inside `drinks.py` the  `available_ingredients` array).
Therefore you have to edit the `drinks.py` file and set the `available_ingredients` array. Each String inside the array represents the ingredientid from the `ingredients` dictionary at the valve corresponding to the index inside the array.
Only drinks that have all the required ingredients set in the `available_ingredients` array will be shown in the menu.


Example:

	available_ingredients = ["gren", "rum", "vodka", "gin", "tequila", "gibe", "lime", "tonic", "mate", "gga", "pine", "oj"]



Development on non-Hector hardware :
---

In the `HectorServer.py` you have to comment line :
	
	#from HectorHardware import HectorHardware as Hector

and uncomment:

	from HectorSimulator import HectorSimulator as Hector


---
Special thanks to
<div>

  <a href="https://www.jetbrains.com/pycharm/">
    <img alt="PyCharm" width="128" heigth="128" hspace="40" src="./images/PyCharm_logo.png">
  </a>

</div>

