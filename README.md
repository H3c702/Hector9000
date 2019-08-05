HECTOR 9000
======================

Minimal Requirements
---

	- Python 3
	- Kivy 
	- RaspberryPi 3

Install on RaspberryPi
----

First of all you have to install Python 3 and Kivy on your Raspberry Pi. 

For this there  is a HowTo on the Kivy Homepage : 		

	https://kivy.org/doc/stable/installation/installation-rpi.html

After you have installed Python and Kivy you can get the sources by using Git

	git clone https://github.com/H3c702/Hector9000.git

You can install all the requirements listed in the file `requirements.txt` by using `pip` (use `pip3` if `pip` uses Python 2)

	pip3 install -r requirements.txt

Start Hector :

	cd Hector9000
	cd srv
	python3 main.py

Add Drinks
---

To add a new Drink you have to modify the `drinks.py` file and add a new item into the array

	{
        "name": "NAME OF DRINK",
        "recipe": [
            ("INGREDIENT1", AMOUNT1),
            ("INGREDIENT2", AMOUNT2)
        ]	
    }

All strings in `UPPERCASE` are placeholders, all lowercase strings have to be used literally in the definition. The `INGREDIENTx` names are not cleartext but are identifiers referencing into the `ingredients` list below in the same file. The `AMOUNTx` values are numerical values of the corresponding ingredient's amount in grams.

At the moment there are only some ingredients but feel free to put in some new.

	# "NAME":("NICENAME", ISALCOHOLIC)
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

Here each ingredient identifier is mapped into a tuple containing the NICENAME used in the UI and a flag that tells whether the ingredient contains alcohol.
A future extension might allow multi-language UIs.

Assigning valves
---

So because Hector has twelve valve channels you have 12 valves predefined (in `servo_config.json` and `HectorHardware.py`) to manage the mapping of each ingredient to a valve.
Therefore you have to edit the `servo_config.json` file and set the `value` field to the ingredient identifier you put into the channel. 
Only drinks that have all the required ingredients set in the `servo_config.json` will be shown in the menu.


Example:

	"pump_3": {
		"name": "Pump 3",
		"channel": 2,
		"value": "oj"
	},



Development on non-Hector hardware :
---

If you are not on the "real" Hector hardware you can set the var `devEnvironment` in `Hectorhardware.py` to `True`:

	devEnvironment = True

The HectorHardware library will then emulate Hector's hardware to allow testing of the UI, for example.

If you are in production or are developing directly on Hector's Pi you should set this var to `False`.
