HECTOR 9000
======================

Min requirements
---

	- Python 3
	- Kivy 
	- RaspberryPi 3

Install on RaspberryPi
----
First of all you have to install Python3 and Kivi on your RaspberryPi. 
For this there  is a HowTo on the Kivi Homepage : 		

	https://kivy.org/doc/stable/installation/installation-rpi.html

After you habe installed Python and Kivy you can get you the sources by using Git

	git clone https://github.com/H3c702/Hector9000.git

have to install all the requiremets listend in the requirement.txt by using pip

	pip3 install -r requirements.txt

Add Drinks
---

To add a new Drink you have to modify the drinks.py file and add a new item in the Array

	{
        "name": "NAME OF DRINK",
        "recipe": [
            ("tequila", 50),
            ("ingredients", ML)
        ]	}

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
		"gren": ("Orange Juice", False),
		"mmix": ("Margarita Mix", True)


Set value of pumps
---

So because you have 12 pumps predefined (servo_config.json and HectorHardware) you have to manage the ingredients of the pumps.
Therefore you have to edit the "servo_config.json" fiel and set the "value" to the ingredients you put in. 
Only drinks that habe all the ingredients it needs where set in the "servo_config.json" will be shown in the Menu.

Example:

	"pump_3": {
		"name": "Pump 3",
		"channel": 2,
		"value": "oj"
	},


Development on not Pi-Mashine :
--

	If you are on a not RaspberryPi you can set the Var in Hectorhardware.py 

	devenvirement = True

	If you are in Production or dev direct on a Pi you can set this var to False.
